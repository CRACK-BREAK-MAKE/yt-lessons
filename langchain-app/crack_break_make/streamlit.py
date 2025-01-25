import streamlit as st
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, SystemMessage

# set page title
st.title("AI Assistant")

# Sidebar
model = st.sidebar.text_input(label="Enter Ollama model", value="llama3.1:latest")

# Initialize state for chat messages
if "messages" not in st.session_state:
	st.session_state.messages = []

if model:
	# Display existing chat history
	for message in st.session_state.messages:
		with st.chat_message(message["role"]):
			st.markdown(message["content"])
			
	# Create chat chain
	llm = ChatOllama(model=model)
	prompt = ChatPromptTemplate.from_messages(
		[
			SystemMessage(content="You are a helpful assistant."),
			MessagesPlaceholder(variable_name="history"),
			HumanMessage(content="{user_query}")
		])
	chain = prompt.pipe(llm)
	
	# User input
	if prompt := st.chat_input(placeholder="How can I help you today?"):
		st.session_state.messages.append({"role": "user", "content": prompt})
		with st.chat_message("user"):
			st.markdown(prompt)
	
	# Prepare chat history
	history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
	
	# Stream the response
	with st.chat_message("assistant"):
		response_stream = chain.stream({"user_query": prompt, "history": history})
		response = st.write_stream(response_stream)
	
	# Append full response to messages
	st.session_state.messages.append({"role": "assistant", "content": response})

else:
	st.info("Please enter an Ollama model name in the sidebar to continue.", icon="⚠")
