import time
import grpc
import logging
import traceback
import user_pb2
import user_pb2_grpc
from concurrent import futures
from database.config import engine
from sqlalchemy import insert, text, values, select, update, delete, desc

from model.user import User

class UserService (user_pb2_grpc.UserServiceServicer):
    def create (self, request, context):
        try:
            with engine.connect() as db:
                db.begin()
                response = db.execute(
                    insert(User).values(
                        role = request.role,
                        name = request.name,
                        email = request.email,
                        address = request.address,
                        password = request.password,
                        phone_number = request.phone_number
                    )
                )
                db.commit()

                if response is None:
                    context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                    return user_pb2.UserCreateRes(
                        user = None,
                        msg = "Gagal Menambahkan Pengguna"
                    )
                    
                return user_pb2.UserCreateRes(
                    user = user_pb2.User(
                        role = request.role,
                        name = request.name,
                        email = request.email,
                        address = request.address,
                        password = request.password,
                        phone_number = request.phone_number,
                        id = response.inserted_primary_key_rows[0][0],
                    ),
                    msg = "Berhasil Menambahkan Pengguna"
                )
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            context.set_code(grpc.StatusCode.UNKNOWN)
            return

    def readAll (self, request, context):
        try:
            with engine.connect() as db:
                response = db.execute(
                    select(User).order_by(desc(User.id))
                )
                users = []
                
                for row in response:
                    users.append(
                        user_pb2.User(
                            id = row[0],
                            role = row[1],
                            name = row[2],
                            email = row[3],
                            address = row[4],
                            password = row[5],
                            phone_number = row[6],
                        )
                    )
                return user_pb2.UserAllRes(
                    user = users,
                    msg = "Berhasil Mendapatkan Daftar Pengguna"
                )

        except Exception as e:
            print(e)
            print(traceback.format_exc())
            context.set_code(grpc.StatusCode.UNKNOWN)
            return

    def readOne (self, request, context):
        try:
            with engine.connect() as conn:
                response = conn.execute(
                    select(User).where(User.id == request.id)
                ).first()
                
                conn.commit()

                if response is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    return user_pb2.UserOneRes(
                        user = None,
                    )

                return user_pb2.UserOneRes(
                    user = user_pb2.User(
                        id = response[0],
                        role = response[1],
                        name = response[2],
                        email = response[3],
                        address = response[4],
                        password = response[5],
                        phone_number = response[6],
                    )
                )
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            context.set_code(grpc.StatusCode.UNKNOWN)
            return

    def update (self, request, context):
        try:
            with engine.connect() as db:
                db.begin()
                response = db.execute(
                    update(User)
                    .where(User.id == request.id)
                    .values(
                        role = request.role,
                        name = request.name,
                        email = request.email,
                        address = request.address,
                        password = request.password,
                        phone_number = request.phone_number
                    )
                )
                db.commit()

                if response is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    return user_pb2.UserUpdateRes(
                        user = None,
                        msg = "Gagal Memperbaharui User"
                    )

                return user_pb2.UserUpdateRes(
                    user = user_pb2.User(
                        id = request.id,
                        role = request.role,
                        name = request.name,
                        email = request.email,
                        address = request.address,
                        password = request.password,
                        phone_number = request.phone_number
                    )
                )
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            context.set_code(grpc.StatusCode.UNKNOWN)
            return

    def delete (self, request, context):
        try:
            with engine.connect() as db:
                db.begin()
                response = db.execute(
                    delete(User).where(User.id == request.id)
                )
                db.commit()

                if response is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    return user_pb2.UserDeleteRes(msg = "Gagal Menghapus User")

                return user_pb2.UserDeleteRes(msg = "Berhasil Menghapus User")
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            context.set_code(grpc.StatusCode.UNKNOWN)
            return

def serve ():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port("localhost:5006")
    server.start()
    print("Server started, listening on 5006")
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    serve()
    