import streamlit as st
from judini import CodeGPTPlus

# Your CodeGPT API details
CODEGPT_API_KEY = "your-api-key"  # Replace with your actual API key
ORG_ID = "your-org-id"            # Replace with your actual Org ID
AGENT_ID = "0000000-0000-0000-0000-000000000000"  # Replace with your actual Agent ID

# Initialize the CodeGPTPlus instance
codegpt = CodeGPTPlus(api_key=CODEGPT_API_KEY, org_id=ORG_ID)

# Function to get response from CodeGPT agent
def get_ai_response(messages):
    # Send the user message to the AI agent for a non-streaming response
    response = codegpt.chat_completion(agent_id=AGENT_ID, messages=messages)
    return response['choices'][0]['message']['content'] if 'choices' in response else "Sorry, something went wrong."

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
