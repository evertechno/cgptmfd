import streamlit as st
from judini import CodeGPTPlus
import json

# Access credentials from Streamlit secrets
API_KEY = st.secrets["codegpt"]["API_KEY"]
ORG_ID = st.secrets["codegpt"]["ORG_ID"]
AGENT_ID = st.secrets["codegpt"]["AGENT_ID"]

# Initialize the CodeGPTPlus instance
codegpt = CodeGPTPlus(api_key=API_KEY, org_id=ORG_ID)

# Function to get response from CodeGPT agent (Non-streaming)
def get_ai_response(messages):
    try:
        # Send the user message to the AI agent for a non-streaming response
        response = codegpt.chat_completion(agent_id=AGENT_ID, messages=messages)
        
        # Print the full response for debugging
        st.write("Full API Response:", json.dumps(response, indent=2))
        
        # Check if the response contains the expected structure
        if 'choices' in response and len(response['choices']) > 0:
            return response['choices'][0]['message']['content']
        else:
            # Log unexpected response format
            st.error(f"Unexpected response format: {json.dumps(response, indent=2)}")
            return "Sorry, something went wrong. Please try again later."
    except Exception as e:
        # Handle any exceptions and show the error
        st.error(f"An error occurred: {str(e)}")
        return "Sorry, an error occurred. Please try again later."

# Function to get response from CodeGPT agent (Streaming)
def get_ai_streaming_response(messages):
    try:
        # Display the streaming chunks as they arrive
        response_text = ""
        for chunk in codegpt.chat_completion(agent_id=AGENT_ID, messages=messages, stream=True):
            response_text += chunk['choices'][0]['message']['content']
            st.write(response_text, end="", flush=True)
        return response_text
    except Exception as e:
        # Handle any exceptions and show the error
        st.error(f"An error occurred: {str(e)}")
        return "Sorry, an error occurred. Please try again later."

# Streamlit UI elements
st.title("AI Chatbot")

# Conversation history for session state
if 'history' not in st.session_state:
    st.session_state.history = []

# Display the conversation history
for user_input, ai_response in st.session_state.history:
    st.write(f"**You:** {user_input}")
    st.write(f"**AI:** {ai_response}")

# Input text box for user query
user_input = st.text_input("Your message:")

# Choose whether you want streaming or non-streaming
streaming_mode = st.checkbox("Enable Streaming Mode")

if user_input:
    # Add user's input to the message history
    messages = [{"role": "user", "content": user_input}]
    
    # Get the AI response based on the chosen mode
    if streaming_mode:
        ai_response = get_ai_streaming_response(messages)
    else:
        ai_response = get_ai_response(messages)

    # Store the conversation in history
    st.session_state.history.append((user_input, ai_response))

    # Display the new conversation
    st.write(f"**You:** {user_input}")
    st.write(f"**AI:** {ai_response}")
