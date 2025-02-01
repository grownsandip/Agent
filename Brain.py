import os
import base64
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
#SETTING UP GROQ API KEY
Groq_api_key=os.getenv("GROQ_API_KEY")
#CONVERTING REQUIRED IMAGE TO BASE64
image_path="images/prescription_2.jpg"
image_file=open(image_path,"rb")
print(image_file)
encoded_image=base64.b64encode(image_file.read()).decode('utf-8')
#BUild model
client=Groq()
query="Can you read what is written"
model="llama-3.2-90b-vision-preview"
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
chat_completions=client.chat.completions.create(
    messages=messages,
    model=model,
)
print(chat_completions.choices[0].message.content)