import os
import base64
from groq import Groq
from dotenv import load_dotenv
import json
load_dotenv()
#SETTING UP GROQ API KEY
Groq_api_key=os.getenv("GROQ_API_KEY")
#CONVERTING REQUIRED IMAGE TO BASE64
def image_encoding(image_path):
  with open (image_path,"rb") as image_file:
 #print(image_file)
      encoded_image=base64.b64encode(image_file.read()).decode('utf-8')
  return encoded_image
#BUild model
query="give me the side effects of following medicine"
model="llama-3.2-90b-vision-preview"
def analyze_image(query,model,encoded_image,available_functions):
  client=Groq()
  messages=[{
    "role":"user",
    "content":[
        {
            "type":"text",
            "text":query,
        },
        {
            "type":"image_url",
            "image_url":{
                "url":f"data:image/jpeg;base64,{encoded_image}",
            },
        },
    ],
 }]
  tools=[
    {
      "type": "function",
        "function": {
            "name": "get_medicine_information",
            "description": "Gets information about medicne",
            "parameters": {
                "type": "object",
                "properties": {
                    "medicine_name": {
                        "type": "string",
                        "description": "The name of the particular medicine",
                    }
                },
                "required": ["medicine_name"],
            },
        },
    }
  ]
  chat_completions=client.chat.completions.create(
    messages=messages,
    model=model,
    tools=tools,
    tool_choice="required",
  )
  response_message=chat_completions.choices[0].message
  #print(response_message.tool_calls)
  tool_calls=response_message.tool_calls
  for tool_call in tool_calls:
       # Get the function name from the tool call
        function_name = tool_call.function.name
        # Get the function to call from the available functions dictionary
        function_name = function_name.strip()
        function_to_call = available_functions.get(function_name)
        # Parse the function arguments from the tool call
        function_args = json.loads(tool_call.function.arguments)

        # Call the function with the medicine name
        function_response = function_to_call(
           medicine_name=function_args.get("medicine_name"),
        )
   # Return the response from the called function
  messages.append({
            "tool_call_id": tool_call.id, 
            "role": "tool", # Indicates this message is from tool use
            "name": function_name,
            "content": function_response,
                })
  final_resposnse=client.chat.completions.create(
    model=model,
    messages=messages
  )
  return final_resposnse.choices[0].message.content