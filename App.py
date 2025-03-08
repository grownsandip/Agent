import os
import gradio as gr
from Brain import image_encoding,analyze_image
from input_voice import record_audio,transcribe
from output_voice import text_to_speech_with_gtts
from Tools import get_medicine_information

system_prompt="You are an AI assistant that extracts medicine names from prescriptions and retrieves their details.You MUST extract at least one medicine name and pass it to the get_medicine_information function.If you cannot extract a medicine name, respond with No medicine name found."
def process_inputs(audio_file_path,image_file_path):
    speech_to_text_output=transcribe(audio_filepath=audio_file_path,stt_model="whisper-large-v3")
    available_functions = {
        "get_medicine_information": get_medicine_information
    }
    if image_file_path:
        agent_response=analyze_image(query=speech_to_text_output+system_prompt,encoded_image=image_encoding(image_file_path),model="llama-3.2-11b-vision-preview",available_functions=available_functions)
    else:
        agent_response="No prescription image provided for details"
        
    voice_of_agent=text_to_speech_with_gtts(input_text=agent_response,output_filepath="final.mp3")
    return speech_to_text_output,agent_response,voice_of_agent
    # print(audio_file_path,image_file_path)

iface=gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Agent's Response"),
        gr.Audio("final.mp3",autoplay=True)
    ],
    title="Agent for Prescription reading"
)
iface.launch(debug=True)