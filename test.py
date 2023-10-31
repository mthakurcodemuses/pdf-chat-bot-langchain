from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

chat_model = ChatOpenAI(verbose=True, streaming=True)

prompt = ChatPromptTemplate.from_messages([("human", "{content}")])
messages = prompt.format_messages(content="Hello, how are you?")
print(messages)

output = chat_model(messages)
print(output)