from langchain.callbacks.base import BaseCallbackHandler


class StreamingHandler(BaseCallbackHandler):

    def __init__(self, queue):
        self.queue = queue
        self.streaming_run_ids = set()

    def on_chat_model_start(
            self,
            serialized,
            messages,
            run_id,
            **kwargs):
        print("Run Id of on_chat_model_start: ", run_id)
        if serialized["kwargs"]["streaming"]:
            print("Run Id of streaming model: ", run_id)
            self.streaming_run_ids.add(run_id)

    def on_llm_new_token(
            self,
            run_id,
            token,
            **kwargs):
        print("Run Id inside on_llm_new_token: ", run_id)
        self.queue.put(token)

    def on_llm_end(
            self,
            response,
            run_id,
            **kwargs):
        print("Run Id inside on_llm_end: ", run_id)
        if run_id in self.streaming_run_ids:
            print("Removing run id on llm_end: ", run_id)
            self.streaming_run_ids.remove(run_id)
            self.queue.put(None)

    def on_llm_error(
            self,
            run_id,
            error,
            **kwargs):
        print("Run Id inside on_llm_end: ", run_id)
        if run_id in self.streaming_run_ids:
            print("Removing run id on llm_error: ", run_id)
            self.streaming_run_ids.remove(run_id)
            self.queue.put(None)
