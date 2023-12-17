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


# setup grpc server
cd grpc_server


python -m venv ./product/env
./product/env/Scripts/activate.bat
./product/env/Scripts/pip install -e ./product
./product/env/Scripts/deactivate.bat