class AgentSettings:
    prompt: str
    output_type: str | None = None
    model: str

class Agent:
    def __init__(self, settings):
        self.prompt = settings.get("prompt")
        self.output_type = settings.get("output_type", None)
        self.model = settings.get("model")
        self.reasoning = settings.get("reasoning", None)


async def get_completion(client, agent: Agent, input):
    params = dict(
        model=agent.model,
        instructions=agent.prompt,
        input=str(input),
        # tools=tools,
        # tool_choice=tool_settings
    )

    if agent.reasoning:
        params["reasoning"] = {"effort": agent.reasoning}

    # if output_format:
    #     params["text"] = output_format

    response = await client.responses.create(**params)
    return response.output_text

