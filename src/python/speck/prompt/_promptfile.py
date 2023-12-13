class Promptfile:
    """A class for loading and parsing .prompt files"""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.promptfile = self._load_promptfile()

    def _load_promptfile(self) -> dict:
        """Load the promptfile from the filepath."""
        return {}

    def _parse_promptfile(self) -> dict:
        """Parse the promptfile."""
        return {}
