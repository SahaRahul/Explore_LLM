from flask import (
    Flask,
    render_template,
    request,
    Response,
    stream_with_context,
    jsonify,
)
import os
import asyncio
from openai import OpenAI
from flask_cors import CORS

from langchain import  SQLDatabase
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain_community.callbacks import get_openai_callback
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.callbacks import BaseCallbackManager

from langchain.agents import AgentExecutor
import threading
import queue

# Custom callback handler to stream tokens
class StreamingCallbackHandler(BaseCallbackHandler):
    def __init__(self, token_queue):
        self.token_queue = token_queue

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        data = token.replace('\n', ' <br> ')
        self.token_queue.put(f"data: {data}\n\n")

    def on_agent_finish(self, finish, **kwargs) -> None:
        self.token_queue.put(None)  # Signal the end of streaming


OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# client = openai.OpenAI()

llm_model = "gpt-3.5-turbo"
llm = ChatOpenAI(temperature=0.0, model=llm_model, stream=True)

# Create db chain

# Setup database
db = SQLDatabase.from_uri(
    f"postgresql+psycopg2://postgres:welcome@localhost:5432/postgres",
)

QUERY = """
Given an input question, first create a syntactically correct postgresql query to run, /
then look at the results of the query and return the answer from the table.
Use the following format:

"Question": "Question here"
"Verify": "Show me which database you are referring"
"SQLQuery": "SQL Query to run"
"SQLResult": "Result of the SQLQuery"
"Answer": "Final answer here"

"{question}"
"""

# Setup the SQLDatabase Toolkit and agent

app = Flask(__name__)
CORS(app)

chat_history = [
    {"role": "system", "content": "You are a helpful assistant."},
]

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", chat_history=chat_history)

@app.route("/chat", methods=["POST"])
def chat():
    content = request.json.get("message")
    chat_history.append({"role": "user", "content": content})
    return jsonify(success=True)

# @app.route("/stream", methods=["GET"])
# def stream():
#     def generate():
#         assistant_response_content = ""
#         finished = False

#         QUERY = """
#         Given an input question, first create a syntactically correct postgresql query to run, /
#         then look at the results of the query and return the answer from the table.
#         Use the following format:

#         "Question": "Question here"
#         "Verify": "Show me which database you are referring"
#         "SQLQuery": "SQL Query to run"
#         "SQLResult": "Result of the SQLQuery"
#         "Answer": "Final answer here"

#         "{question}"
#         """

#         question = QUERY.format(question=assistant_response_content)

#         with get_openai_callback() as cb:
#             stream = agent_executor.run(question)

#         # with client.chat.completions.create(
#         #     model="gpt-4-turbo",
#         #     messages=chat_history,
#         #     stream=True,
#         # ) as stream:
            
#             print(stream)

#             for chunk in stream:
#                 if chunk.choices[0].delta and chunk.choices[0].delta.content:
#                     content = chunk.choices[0].delta.content
#                     assistant_response_content += content
#                     data = chunk.choices[0].delta.content.replace('\n', ' <br> ')
#                     yield f"data: {data}\n\n"


#                 if chunk.choices[0].finish_reason == "stop":
#                     finished = True
#                     break  
        
#         yield f"data: finish_reason: stop\n\n"
#         chat_history.append({"role": "assistant", "content": assistant_response_content})
#         if finished:
#             return

#     return Response(stream_with_context(generate()), mimetype="text/event-stream")

@app.route("/stream", methods=["GET"])
def stream():
    def generate():
        # token_queue = queue.Queue()

        # Create db chain
        QUERY = """
        Given an input question, first create a syntactically correct postgresql query to run, /
        then look at the results of the query and return the answer from the table.
        Use the following format:

        "Question": "Question here"
        "Verify": "Show me which database you are referring"
        "SQLQuery": "SQL Query to run"
        "SQLResult": "Result of the SQLQuery with minimal text"
        "Answer": "Final answer here"

        "{question}"
        """

        # # Setup the database chain
        # db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)

        toolkit = SQLDatabaseToolkit(db=db, llm=llm)

        agent_executor = create_sql_agent(
            llm=llm,
            toolkit=toolkit,
            verbose=True,
            handle_parsing_errors=True
        )

        def get_prompt():
            
            print("Type 'exit' to quit")

            # while True:
            prompt = chat_history[-1]
            print(prompt)

            # if prompt.lower() == 'exit':
            #     print('Exiting...')
            #     break
            # else:
            try:
                question = QUERY.format(question=prompt)

                # with get_openai_callback() as cb:
                result = agent_executor.run(question)
                
                print("SQL Query Result:")
                print(result)
                # yield f"data: {result.split(':')}\n\n"
                # await asyncio.sleep(3)
                return result
            except Exception as e:
                print("-----exception-----",e)
                pass
                finished = True
                # await asyncio.sleep(3)
                return finished
        
        assistant_response_content = get_prompt()
        if assistant_response_content:
            chat_history.append({"role": "assistant", "content": assistant_response_content})
            # yield f"data: role: assistant, content: {assistant_response_content}\n\n"
            yield f"data: {assistant_response_content}\n\n"
        else:
            yield f"data: finish_reason: stop\n\n"

    return Response(stream_with_context(generate()), mimetype="text/event-stream")


@app.route("/reset", methods=["POST"])
def reset_chat():
    global chat_history
    chat_history = [{"role": "system", "content": "You are a helpful assistant."}]
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(port=5000)