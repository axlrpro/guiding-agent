import subprocess
import sys
import tempfile
import os
from google.adk.agents import Agent

def execute_python_code(code: str):
    """
    Runs python code in a separate process.
    Input: code (as a string)
    """
    code = clean_python_code(code)

    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_script:
            temp_script.write(code)
            script_path = temp_script.name
        
        print(f"Running code in a separate process via {script_path}...")
        
        process = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            check=True
        )

        print("Subprocess stdout:", process.stdout)
        return {"result": "success", "output": process.stdout}

    except subprocess.CalledProcessError as e:
        print("Subprocess stderr:", e.stderr)
        return {"result": "failure", "reason": e.stderr}
    except Exception as e:
        return {"result": "failure", "reason": str(e)}
    finally:
        if 'script_path' in locals() and os.path.exists(script_path):
            os.remove(script_path)
        
def clean_python_code(code_string: str):
    """Cleans up python code. To be used before python code execution

    Args:
        code_string (str): code to clean
    Output: 
        cleaned code(str)
    """
    prefix = "```python"
    suffix = "```"

    cleaned_code = code_string.strip()

    if cleaned_code.startswith(prefix):
        cleaned_code = cleaned_code[len(prefix):].strip()

    if cleaned_code.endswith(suffix):
        cleaned_code = cleaned_code[:-len(suffix)].strip()
        
    cleaned_code = cleaned_code.strip()

    return cleaned_code
    
code_runner = Agent(
    name="code_runner",
    model="gemini-2.0-flash",
    description="Runs python code.",
    instruction='''You are code runner agent.
    Execute the following code using the execute_python_function tool provided.
    {code}
    You have access to the 'execute_python_code' function which can execute the code
    The function expects only one input, the code as a string
    The output from the function will of the following type:
    Successful execution:
    {
        "status":"success"
    }
    
    Unsuccessful execution:
    {
        "status":"failure",
        "reason": <reason for failure will be mentioned here>
    }
    Display the output to the user as follows:
    In case successful:
    "Hi I'm the Code Executor. The provided code has been executed successfully."
    
    In case of failed execution:
    "Hi I'm the Code Executor. The provided code execution failed. Reason: <provide reason>."
    ''',
    tools=[execute_python_code]
)