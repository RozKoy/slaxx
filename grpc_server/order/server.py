import time
import grpc
import logging
import traceback
import order_pb2
import order_pb2_grpc
from concurrent import futures
from database.config import engine
from sqlalchemy import insert, text, values, select, update, delete, desc

from model.order import Order

class OrderService (order_pb2_grpc.OrderServiceServicer):
    def create (self, request, context):
        try:
            with engine.connect() as db:
                db.begin()
                response = db.execute(
                    insert(Order).values(
                        status = request.status,
                        item_count = request.item_count,
                        price_count = request.price_count,
                        create_at = request.create_at,
                        customerId = request.customerId,
                    )
                )
                db.commit()

                if response is None:
                    context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                    return order_pb2.OrderCreateRes(
                        order = None,
                        msg = "Gagal Menambahkan Order"
                    )
                    
                return order_pb2.OrderCreateRes(
                    order = order_pb2.Order(
                        status = request.status,
                        item_count = request.item_count,
                        price_count = request.price_count,
                        create_at = request.create_at,
                        customerId = request.customerId,
                        id = response.inserted_primary_key_rows[0][0],
                    ),
                    msg = "Berhasil Menambahkan Order"
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
                    select(Order).order_by(desc(Order.id))
                )
                order = []
                
                for row in response:
                    order.append(
                        order_pb2.Order(
                            id = row[0],
                            status = row[1],
                            item_count = row[2],
                            price_count = row[3],
                            create_at = row[4],
                            customerId = row[5],
                        )
                    )
                return order_pb2.OrderAllRes(
                    order = order,
                    msg = "Berhasil Mendapatkan Daftar Order"
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
                    select(Order).where(Order.id == request.id)
                ).first()
                
                conn.commit()

                if response is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    return order_pb2.OrderOneRes(
                        order = None,
                    )

                return order_pb2.OrderOneRes(
                    order = order_pb2.Order(
                        id = response[0],
                        status = response[1],
                        item_count = response[2],
                        price_count = response[3],
                        create_at = response[4],
                        customerId = response[5],
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
                    update(Order)
                    .where(Order.id == request.id)
                    .values(
                        status = request.status,
                        item_count = request.item_count,
                        price_count = request.price_count,
                        customerId = request.customerId,
                    )
                )
                db.commit()

                if response is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    return order_pb2.OrderUpdateRes(
                        order = None,
                        msg = "Gagal Memperbaharui Order"
                    )

                return order_pb2.OrderUpdateRes(
                    order = order_pb2.Order(
                        id = request.id,
                        status = request.status,
                        item_count = request.item_count,
                        price_count = request.price_count,
                        customerId = request.customerId,
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
                    delete(Order).where(Order.id == request.id)
                )
                db.commit()

                if response is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    return order_pb2.OrderDeleteRes(msg = "Gagal Menghapus Order")

                return order_pb2.OrderDeleteRes(msg = "Berhasil Menghapus Order")
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            context.set_code(grpc.StatusCode.UNKNOWN)
            return

def serve ():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    order_pb2_grpc.add_OrderServiceServicer_to_server(OrderService(), server)
    server.add_insecure_port("localhost:5007")
    server.start()
    print("Server started, listening on 5007")
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    serve()
    