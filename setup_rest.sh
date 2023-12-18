# create root env
python -m venv ./rest/env

# setup rest
./rest/env/Scripts/activate.bat
./rest/env/Scripts/pip install -e ./rest

# generate proto
./env/Scripts/python -m grpc_tools.protoc -I./grpc --python_out=./rest/rest/grpc_client/order --pyi_out=./rest/rest/grpc_client/order --grpc_python_out=./rest/rest/grpc_client/order ./grpc/order.proto
./env/Scripts/python -m grpc_tools.protoc -I./grpc --python_out=./rest/rest/grpc_client/orderlist --pyi_out=./rest/rest/grpc_client/orderlist --grpc_python_out=./rest/rest/grpc_client/orderlist ./grpc/orderlist.proto
./env/Scripts/python -m grpc_tools.protoc -I./grpc --python_out=./rest/rest/grpc_client/product --pyi_out=./rest/rest/grpc_client/product --grpc_python_out=./rest/rest/grpc_client/product ./grpc/product.proto
./env/Scripts/python -m grpc_tools.protoc -I./grpc --python_out=./rest/rest/grpc_client/user --pyi_out=./rest/rest/grpc_client/user --grpc_python_out=./rest/rest/grpc_client/user ./grpc/user.proto


./rest/env/Scripts/deactivate.bat