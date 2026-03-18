import os
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
 
API_KEY = os.getenv("MISTRAL_API_KEY")

MODEL = "mistral-medium-latest"

# Sampling parameters
# Low temperature = more deterministic (good for tool calling)
# The docs recommend altering temperature OR top_p, not both.

TEMPERATURE = 0.1
TOP_P = 0.9

# Agent loop safety cap

MAX_ITERATIONS = 5

# Mistral client (single instance, reused everywhere)

client = Mistral(api_key=API_KEY)