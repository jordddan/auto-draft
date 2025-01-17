import openai
import re
import os
import json
import logging
log = logging.getLogger(__name__)

openai.api_key = os.environ['OPENAI_API_KEY']

def extract_responses(assistant_message):
    # pattern = re.compile(r"f\.write\(r'{1,3}(.*?)'{0,3}\){0,1}$", re.DOTALL)
    pattern = re.compile(r"f\.write\(r['\"]{1,3}(.*?)['\"]{0,3}\){0,1}$", re.DOTALL)
    match = re.search(pattern, assistant_message)
    if match:
        return match.group(1)
    else:
        log.info("Responses are not put in Python codes. Directly return assistant_message.\n")
        log.info(f"assistant_message: {assistant_message}")
        return assistant_message

def extract_keywords(assistant_message, default_keywords=None):
    if default_keywords is None:
        default_keywords = {"machine learning":5}

    try:
        keywords = json.loads(assistant_message)
    except ValueError:
        log.info("Responses are not in json format. Return the default dictionary.\n ")
        log.info(f"assistant_message: {assistant_message}")
        return default_keywords
    return keywords

def extract_section_name(assistant_message, default_section_name=""):
    try:
        keywords = json.loads(assistant_message)
    except ValueError:
        log.info("Responses are not in json format. Return None.\n ")
        log.info(f"assistant_message: {assistant_message}")
        return default_section_name
    return keywords


def extract_json(assistant_message, default_output=None):
    if default_output is None:
        default_keys = ["Method 1", "Method 2"]
    else:
        default_keys = default_output
    try:
        dict = json.loads(assistant_message)
    except:
        log.info("Responses are not in json format. Return the default keys.\n ")
        log.info(f"assistant_message: {assistant_message}")
        return default_keys
    return dict.keys()


def get_responses(user_message, model="gpt-4", temperature=0.4):
    conversation_history = [
        {"role": "system", "content": "You are an assistant in writing machine learning papers."}
    ]
    conversation_history.append({"role": "user", "content": user_message})
    response = openai.ChatCompletion.create(
        model=model,
        messages=conversation_history,
        n=1,  # Number of responses you want to generate
        temperature=temperature,  # Controls the creativity of the generated response
    )
    assistant_message = response['choices'][0]["message"]["content"]
    usage = response['usage']
    log.info(assistant_message)
    return assistant_message, usage


if __name__ == "__main__":
    test_strings = [r"f.write(r'hello world')", r"f.write(r'''hello world''')", r"f.write(r'''hello world",
                     r"f.write(r'''hello world'", r'f.write(r"hello world")', r'f.write(r"""hello world""")',
                     r'f.write(r"""hello world"', r'f.write(r"""hello world']
    for input_string in test_strings:
        print("input_string: ", input_string)
        pattern = re.compile(r"f\.write\(r['\"]{1,3}(.*?)['\"]{0,3}\){0,1}$", re.DOTALL)

        match = re.search(pattern, input_string)
        if match:
            extracted_string = match.group(1)
            print("Extracted string:", extracted_string)
        else:
            print("No match found")