import traceback
import re
import functools
from chatGPT_debugger.callAPI import call_chatGPT
import os


def debug(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print()
            print()
            tb = traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
            error = tb[-2]
            pattern = re.compile(r'line \d+')
            line_number = list(pattern.finditer(error))[0][0]
            
            
            print(f"chatGPT Detected an error in {line_number}")
            print("#" * 100)
            print()
            print(f"\033[31mError Message: {error}\033[0m")
            print("#" * 75)
            
            function_name = re.search(r'in\s+(\w+)', error).group(1)
            
            if function_name == func.__name__:
                response = call_chatGPT(func,line_number,e)
                print("_" * 75)
                print(response)
                print(f"_" * 75)
        
            elif function_name in globals():
                print()
                print(f"""\n\033[31mThe Error Occurs in a Function Called {function_name}.\n
                But That particular Function was not Decareted. So ChatGPT can't Provide
                a Better Solution. Please Decarate That Function And Try Again...\033[0m
                """)
                
            else:
                response = call_chatGPT(func)
                print("_" * 75)
                print(response)
                print(f"_" * 75)

    return wrapper