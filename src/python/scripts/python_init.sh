#!/bin/zsh

# Check if venv exists. If it does, delete it
if [ -d "venv" ]; then
    rm -rf venv
fi

# Check pyenv command
if command -v pyenv 1>/dev/null 2>&1; then
    pyenv local 3.12
fi

# Install venv and requirements
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}.:./src/python"
