import streamlit as st
from backend import get_response
from PIL import Image
import json



st.set_page_config(layout="centered")
def scroll_to_bottom():
    st.components.v1.html("""
        <script>
            window.scrollTo(0, document.body.scrollHeight);
        </script>
    """, height=0, width=0)

if "messages" not in st.session_state:
    st.session_state.messages=[]
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = {"images": [], "pdfs": []}
def chat_section():
    st.header("Chat with Agent and get your files")
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
                st.write(message["content"])
    scroll_to_bottom()
                
def prompt_section():
    user_input = st.chat_input("Enter your instructions here")
    if user_input:
        # Display user input immediately
        st.session_state["messages"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Placeholder for the agent's response
        response_placeholder = st.chat_message("agent")
        response_container = response_placeholder.container()

        # Stream agent response
        agent_response = ""
        with st.spinner("Generating response..."):
            for chunk in get_response(user_input):  # Assume `get_response` yields chunks
                agent_response += chunk
            response_container.write(agent_response)

        # Store the final response
        st.session_state["messages"].append({"role": "agent", "content": agent_response})
    
def upload_sections():
    File_preview=st.empty()
    if "images" in st.session_state.uploaded_files:
        st.session_state.uploaded_files["images"].clear()
    if "pdfs" in st.session_state.uploaded_files:
        st.session_state.uploaded_files["pdfs"].clear()
    uploaded_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    if uploaded_image is not None:
         image=Image.open(uploaded_image)
         width,height=image.size
         File_preview.image(image,caption=f"{width} X {height}")
         st.session_state.uploaded_files["images"].append({
            "file": uploaded_image,
            "name": uploaded_image.name,
            "size": uploaded_image.size,
            "width":width,
            "height":height
        })
    uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])
    if uploaded_pdf is not None:
         st.write(uploaded_pdf.size)
         st.session_state.uploaded_files["pdfs"].append({
            "file": uploaded_pdf,
            "name": uploaded_pdf.name,
            "size": uploaded_pdf.size
        })
def collect_file_details():
    if st.session_state.uploaded_files["images"] or st.session_state.uploaded_files["pdfs"]:
        file_details = {
            "images": [
                {
                    "name": img["name"],
                    "size": img["size"],
                    "width": img["width"],
                    "height": img["height"]
                } for img in st.session_state.uploaded_files["images"]
            ],
            "pdfs": [
                {
                    "name": pdf["name"],
                    "size": pdf["size"]
                } for pdf in st.session_state.uploaded_files["pdfs"]
            ]
        }

        # Convert file details to a JSON string
        file_details_json = json.dumps(file_details, indent=2)

        # Display file details
        #st.write("Uploaded Files:")
        #st.json(file_details_json)

        # Pass file detail
        return file_details_json
    else:
        st.write("No files uploaded.")
        return None

        
def main():
     chat_section()
     prompt_section()
     with st.sidebar:
         upload_sections()
         if st.button("Send Files to agent",use_container_width=True):
             file_details_json = collect_file_details()
             if file_details_json:
                # Create a prompt to send the file details
                prompt = f"The user has uploaded the following files:\n{file_details_json}\nProcess these files and provide a response."
                # Call get_response with the prompt
                response_generator = get_response(prompt)
                st.session_state["messages"].append({"role": "agent", "content": response_generator})
                #for response_chunk in response_generator:
                   # st.write(response_chunk)

    
if __name__=="__main__":
    main()
    
#next task is to reflect the llm prompt into the chat section