# @author Mohan Sharma


from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama

FORMAT_MARKDOWN_PROMPT = """You are a helpful assistant. Please respond to the user's query in Markdown format."""

def main():
	# Step 1: Initialize the LLM
	llm = ChatOllama(model="llama3.1:latest")
	
	# Step 2: Create the prompt template
	prompt = ChatPromptTemplate.from_messages([
		SystemMessagePromptTemplate.from_template(FORMAT_MARKDOWN_PROMPT),
		HumanMessagePromptTemplate.from_template("{user_query}")
	])
	
	# Step 3: Combine the prompt with the LLM into a base chain
	base_chain = prompt.pipe(llm)
	
	while True:
		# Step 4: Take user input
		user_query = input("You: ")
		
		if user_query.lower() in ['exit', 'quit', 'bye']:
			print("Exiting. Goodbye!")
			break
			# Step 5: Invoke the chain with user input
		response = base_chain.invoke({"user_query": user_query})
		
		# Step 6: Print the response
		print(f"Assistant: {response.content}")

if __name__ == "__main__":
	main()
