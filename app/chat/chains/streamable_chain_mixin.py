from queue import Queue
from threading import Thread
from app.chat.callbacks.streaming_handler import StreamingHandler
from flask import current_app


class StreamableChainMixin:
    def stream(self, input):

        queue = Queue()
        handler = StreamingHandler(queue)

        def task(app_context):
            app_context.push()
            self(input, callbacks=[handler])

        Thread(target=task, args=[current_app.app_context()]).start()
        while True:
            token = queue.get()
            if token is None:
                break
            yield token
