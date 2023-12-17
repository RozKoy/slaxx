# create root env
python -m venv env

# activate root env
./env/Scripts/activate.bat

# generate grpc product
./env/Scripts/python -m grpc_tools.protoc -I./grpc --python_out=./grpc_server/product --pyi_out=./grpc_server/product --grpc_python_out=./grpc_server/product ./grpc/product.proto
