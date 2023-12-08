#!/bin/zsh

# Remove build/, dist/, and speck.egg-info/ if they exist
if [ -d "build" ]; then
    rm -rf build
fi

if [ -d "dist" ]; then
    rm -rf dist
fi

if [ -d "speck.egg-info" ]; then
    rm -rf speck.egg-info
fi

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
rm -rf speck.egg-info
rm -rf build
rm -rf dist
