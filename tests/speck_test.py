from speck import chat

print(
    chat.create(
        user_id="test",
        model="gpt4-1106-preview",
        messages=[{"role": "user", "content": "Hello, how are you?"}],
    )
)
