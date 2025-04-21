#!/bin/bash

# pip install --upgrade pip
echo "Setting up Python environment in backend"
cd ./src/backend
uv sync --frozen

cd ../../

echo "Setting up Python environment in frontend"
cd ./src/frontend
uv sync --frozen

cd ../../

echo "dependency setup completed."

# (cd ./src/frontend; pip install -r requirements.txt)


# (cd ./src/backend; pip install -r requirements.txt)


