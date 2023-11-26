from .entities import IConnector


class OpenAIConnector(IConnector):
    def process_message(self, message: str) -> str:
        # Implement the processing logic specific to OpenAI
        return f"Processed by OpenAI: {message}"
