import streamlit as st
from judini import CodeGPTPlus
import json

# Access credentials from Streamlit secrets
API_KEY = st.secrets["codegpt"]["API_KEY"]
ORG_ID = st.secrets["codegpt"]["ORG_ID"]
AGENT_ID = st.secrets["codegpt"]["AGENT_ID"]

# Initialize the CodeGPTPlus instance
codegpt = CodeGPTPlus(api_key=API_KEY, org_id=ORG_ID)

# Function to get response from CodeGPT agent with better error handling
def get_ai_response(messages):
    try:
        # Send the user message to the AI agent for a non-streaming response
        response = codegpt.chat_completion(agent_id=AGENT_ID, messages=messages)
        
        # Check if the response contains the expected structure
        if 'choices' in response and len(response['choices']) > 0:
            return response['choices'][0]['message']['content']
        else:
            # Print the full response if it doesn't match expected structure
            st.error(f"Unexpected response format: {json.dumps(response, indent=2)}")
            return "Sorry, something went wrong. Please try again later."
    except Exception as e:
        # Handle any exceptions and show the error
        st.error(f"An error occurred: {str(e)}")
        return "Sorry, an error occurred. Please try again later."

# Streamlit UI elements
st.title("AI Chatbot")

# Display previous messages and conversation history
if 'history' not in st.session_state:
    st.session_state.history = []

# Display the conversation history
for user_input, ai_response in st.session_state.history:
    st.write(f"**You:** {user_input}")
    st.write(f"**AI:** {ai_response}")

# Input text box for user query
user_input = st.text_input("Your message:")

if user_input:
    # Add user's input to the message history
    messages = [{"role": "user", "content": user_input}]
    
    # Get the AI response using the CodeGPT agent
    ai_response = get_ai_response(messages)

    # Store the conversation in history
    st.session_state.history.append((user_input, ai_response))

    # Display the new conversation
    st.write(f"**You:** {user_input}")
    st.write(f"**AI:** {ai_response}")
