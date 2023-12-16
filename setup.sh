# create root env
python -m venv env

# activate root env
./env/Scripts/activate.bat

# install root dependency
./env/Scripts/pip install -e .

# run migrate
./env/Scripts/alembic upgrade head

# deactivate root env
./env/Scripts/deactivate.bat