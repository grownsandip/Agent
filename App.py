import streamlit as st
from backend import get_response
from PIL import Image



st.set_page_config(layout="centered")
def scroll_to_bottom():
    st.components.v1.html("""
        <script>
            window.scrollTo(0, document.body.scrollHeight);
        </script>
    """, height=0, width=0)

if "messages" not in st.session_state:
    st.session_state.messages=[]
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
    uploaded_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    if uploaded_image is not None:
         image=Image.open(uploaded_image)
         width,height=image.size
         File_preview.image(image,caption=f"{width} X {height}")
    uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])
    if uploaded_pdf is not None:
         st.write(uploaded_pdf.size)
def main():
     chat_section()
     prompt_section()
     with st.sidebar:
         upload_sections()

    
if __name__=="__main__":
    main()
    
#next task is to reflect the llm prompt into the chat section