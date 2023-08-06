import inspect
import os
import keyring
from chatGPT_debugger.engine import get_response 
from chatGPT_debugger.store_api_key import store_api_key

def call_chatGPT(func,line_number,e):
    save_permenant =  os.environ.get("save_flag")
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
    
    api_key,save_permenant = store_api_key()
        
    response = get_response(ques,api_key,save_permenant)

    print("_" * 100)
    return f"\033[32m{response}\033[0m"
    print(f"_" * 100)
