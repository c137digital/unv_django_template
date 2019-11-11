rm -rf ./venv

python3 -m venv ./venv

source activate.sh

pip install --upgrade pip wheel
pip install -e ".[dev]"
