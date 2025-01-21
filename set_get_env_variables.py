import os

os.environ['OPENAI_API_KEY'] = <string>

if 'OPENAI_API_KEY' in os.environ:
    print("OPENAI_API_KEY is set")
else:
    print("OPENAI_API_KEY is not set")

openai_api_key = os.environ.get('OPENAI_API_KEY')
