import os
from langfuse.client import Langfuse

langfuse = Langfuse(
            os.environ.get("LANGFUSE_API_KEY"),
            os.environ.get("LANGFUSE_SECRET_KEY"),
            debug=True)
