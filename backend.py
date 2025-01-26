#this file contains all the backend logic of the agent basically the tools will be used here
from groq import Groq
from dotenv import  load_dotenv
import os
import json
from Tools import process_files
load_dotenv()
system=os.getenv("System_identity")
client = Groq(api_key=os.getenv("GROQ_API_KEY"),)
messages=[{"role":"system","content":system}]
tools = [
    {
        "type": "function",
        "function": {
            "name": "process_files",
            "description": "Retrieve details of uploaded files such as images and PDFs.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_size": {
                        "type": "string",
                        "description": "The size of the file to be uploaded eg 200mb or 20kb."
                    },
                },
                "required": ["file_size"],
            },
        }
    }
]

def get_response(prompt):
 messages.append({"role": "user", "content": prompt})
 try:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        tools=tools,
        tool_choice="auto",
        stream=False,
    )
    response_message=response.choices[0].message
    print(f"The response message from LLM is:{response_message}")
    print(f"The tools called by LLM is:{response_message.tool_calls}")
    if response_message.tool_calls:
        for tool in response_message.tool_calls:
            available_functions={
                "process_files":process_files #passing on the real function
            }
            functionToCall=available_functions[tool.function.name]
            args=json.loads(tool.function.arguments)#loading arguments
            functionResponse=functionToCall(args["file_size"]) #calling the function
            print(f"The function response is:{functionResponse}")
            messages.append({
                "role":"tool",
                "content":functionResponse,
                "tool_call_id":tool.id
            })
    second_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
    )
    if second_response:
        content = second_response.choices[0].message.content
    else:   # Use the initial response if no tool calls were made
        content = response_message.content
    print(f"final content is:{content}")
    yield content
 except Exception as e:
     print(f"an error has occured{e}")
     yield f"Error:{e}"
     