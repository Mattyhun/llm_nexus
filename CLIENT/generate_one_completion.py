import logging as log
from llm_communication.openai_api_interface import call_openai_api, extract_message_content
from llm_communication.huggingface_api_interface import call_huggingface_api, get_generated_text_from_response
from llm_communication.local_api_interface import call_local_api, get_text_from_output

interface_function_map = {
    'openai'     : (call_openai_api, extract_message_content),
    'huggingface': (call_huggingface_api, get_generated_text_from_response),
    'local'      : (call_local_api, get_text_from_output),
}

def generate_one_completion(interface_name, model, prompt):
    """
    Generate one completion from the given prompt and model returns the response content
    """
    if interface_name not in interface_function_map:
        log.error("Unknown interface: %s", interface_name)
        raise ValueError("Unknown interface: %s" % interface_name)

    call_api_func, extract_func = interface_function_map[interface_name]
    
    log.debug("Using interface: %s, model: %s, prompt: %s", interface_name, model, prompt)
    response = call_api_func(model, prompt)
    response_content = extract_func(response.json())
    log.debug(response_content)

    return response_content

if __name__ == "__main__":
    from project_config import initialize_logging
    initialize_logging()
    response = generate_one_completion("openai", "gpt-3.5-turbo","Implement a function that returns the sum of two numbers")
    print(response)