from agents import Agent, Runner, set_default_openai_key

from dotenv import load_dotenv
import os

# Load from .env file
load_dotenv()
set_default_openai_key(os.getenv("OPEN_API_KEY_PERSONAL"))


class Completion:
    def __init__(self, prompt, model):
        self.agent = Agent(name="Assistant",
                           instructions=prompt,
                           model=model
                           )

    async def get_completion(self, context):
        result = await Runner.run(self.agent, str(context))
        return result.final_output
