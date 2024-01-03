from speck import Speck

OPENAI_API_KEY = "sk-..."
client = Speck(api_key=None, api_keys={"openai": OPENAI_API_KEY})


# Universal chat format
from speck import ChatConfig, Message, Prompt, Response

prompt = Prompt(
    messages=[
        Message(role="system", content="Hello, how are you, {name}?"),
        Message(role="user", content="I am doing great, how about you, {bad_person}?"),
    ]
)
config = ChatConfig(
    model="openai:gpt-3.5-turbo",
    temperature=0.0,
    stream=True,
)
response: Response = client.chat.create(prompt=prompt, config=config)


# OpenAI format
from speck import OpenAIChatConfig

config = OpenAIChatConfig(
    model="gpt-3.5-turbo",
    temperature=0.0,
    stream=True,
)

# ...


# Chat logger
client.chat.log(
    messages=Prompt(
        messages=[{"role": "system", "content": "Hello, how are you, {name}?"}],
    ),
    config=ChatConfig(
        model="openai:gpt-3.5-turbo",
    ),
    response="Example output.",
)

# App logger
client.logger.info("Hello, world!")
