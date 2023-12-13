from speck import Prompt

prompt = Prompt(
    messages=[
        {"role": "system", "content": "Hello, how are you, {name}?"},
        {"role": "user", "content": "I am doing great, how about you, {bad_person}?"},
    ]
)

prompt = prompt.format(bad_person="Terrible Person!", name="John")
print(prompt)
