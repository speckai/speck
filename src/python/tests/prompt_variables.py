from speck import Message, Prompt

prompts = Prompt.read_all(path="prompts/greetings.prompt")
intro, ask = prompts["intro"], prompts["ask"]
new_prompt = (
    intro.format(NAME="person")
    + Message(
        role="assistant", content="I am doing great, how about you, {BAD_PERSON}?"
    )
    + ask.format(DATE="today")
)

a = Prompt(messages=[Message(role="system", content="Hello, {NAME}!")])
b = Prompt(messages=[Message(role="system", content="How are you {NAME}?")])
new_prompt = a.format(NAME="Person A") + b.format(NAME="Person A")

print(new_prompt)
