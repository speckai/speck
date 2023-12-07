#!/bin/zsh

if [ -d "dist_venv" ]; then
    rm -rf venv
fi

if command -v pyenv 1>/dev/null 2>&1; then
    pyenv local 3.12
fi

# Install venv and requirements
python -m venv dist_venv
source dist_venv/bin/activate
export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}."
pip install setuptools
pip install wheel
pip install twine

python setup.py sdist bdist_wheel
twine upload dist/*

# Cleanup
deactivate
rm -rf dist_venv
