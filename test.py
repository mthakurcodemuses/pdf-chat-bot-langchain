from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.base import BaseCallbackHandler
from dotenv import load_dotenv
from queue import Queue
from threading import Thread

load_dotenv()


class StreamingHandler(BaseCallbackHandler):

    def __init__(self, queue):
        self.queue = queue

    def on_llm_new_token(
            self,
            token,
            **kwargs):
        self.queue.put(token)

    def on_llm_end(
            self,
            response,
            **kwargs):
        self.queue.put(None)

    def on_llm_error(
            self,
            error,
            **kwargs):
        self.queue.put(None)

class StreamableChain:
    def stream(self, input):

        queue = Queue()
        handler = StreamingHandler(queue)
        def task():
            self(input, callbacks=[handler])

        Thread(target=task).start()
        while True:
            token = queue.get()
            if token is None:
                break
            yield token

class StreamingChain(StreamableChain, LLMChain):
    pass


chat_model = ChatOpenAI(verbose=True, streaming=True)
prompt = ChatPromptTemplate.from_messages([("human", "{content}")])
messages = prompt.format_messages(content="Tell me a joke about science?")
llm_chain = StreamingChain(llm=chat_model, prompt=prompt, verbose=True)
for output in llm_chain.stream(input=messages):
    print(output)
