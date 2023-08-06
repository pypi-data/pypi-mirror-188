import inspect
import os
import keyring
from chatGPT_debugger.engine import get_response 


def call_chatGPT(func,line_number,e):
    source = inspect.getsource(func)
    ques = f"""I'm Stuggling with an Error in line {line_number}, the error says \n {e}. and Here is the code 
    {source} \n\n
    please provide the answer with these informations:
        01. why this error occurs (Note: Give Indepth Explanation)
        02. how to fix this error
        03. Corrected Code
        
    Also when you submitting the output don't write my notes again
    """
    ques = ques.replace("@debug" ,"")

    api_key = keyring.get_credential(service_name="chatGPT_debugger",username=None)
    
    if api_key is None or api_key.password == "null":
        api_key = input("Enter your OpenAI API key: ")
        keyring.set_password(service_name="chatGPT_debugger",username="User",password=api_key)
    else:
        api_key = api_key.password
        
    response = get_response(ques,api_key)

    print("_" * 100)
    return f"\033[32m{response}\033[0m"
    print(f"_" * 100)
