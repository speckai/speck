from speck.models import chat

print(
    "Nice:",
    chat.create_stream(
        model="gpt-4-1106-preview",
        messages=[{"role": "user", "content": "Hello, how are you?"}],
        process_chunk_lambda=lambda text, chunk: print(text, chunk),
    ),
)
