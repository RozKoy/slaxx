# Slaxx RESTFUL API
**Slaxx RESTFUL API** - Application Programming Interface for slaxx clothes commerce. Create, Read, Update and Delete process for Product and User

## Dependencies
- **`Python > v3.8`**

- **`JavaScript@latest`**

- **`Nodemon`**

## How to run
- Clone this repository

```
git clone https://github.com/RozKoy/slaxx.git
```

- open slaxx directory

```
cd slaxx
```

- make database with name `slaxx`

- run setup

```
./setup.sh
./setup_grpc.sh
./setup_rest.sh
```

- run all server, folder: /grpc_server/**/

```
nodemon --exec ./env/Scripts/python server.py
```

- run pyramid framework in folder /rest/

```
ngrok http --domain=ruling-quetzal-noticeably.ngrok-free.app 6543
```
