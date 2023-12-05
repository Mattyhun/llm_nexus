import os
import set_env_vars
from llm_communicator import LLMCommunicator

# Környezeti változók használata
api_key = os.environ.get('GPT3_API_KEY')
api_url = os.environ.get('GPT3_API_URL')  # Például: 'https://api.openai.com/v1/engines/davinci-codex/completions'
api_model = "gpt-3.5-turbo"
# LLMCommunicator példányosítása
communicator = LLMCommunicator(api_key, api_url, api_model)


response = communicator.send_request('Implement a function that returns the sum of two numbers')

print(response)