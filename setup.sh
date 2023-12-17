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

python -m venv ./user/env
./user/env/Scripts/activate.bat
./user/env/Scripts/pip install -e ./user
./user/env/Scripts/deactivate.bat

python -m venv ./order/env
./order/env/Scripts/activate.bat
./order/env/Scripts/pip install -e ./order
./order/env/Scripts/deactivate.bat

python -m venv ./orderlist/env
./orderlist/env/Scripts/activate.bat
./orderlist/env/Scripts/pip install -e ./orderlist
./orderlist/env/Scripts/deactivate.bat