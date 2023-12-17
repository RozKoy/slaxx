import time
import grpc
import logging
import traceback
import orderlist_pb2
import orderlist_pb2_grpc
from concurrent import futures
from database.config import engine
from sqlalchemy import insert, text, values, select, update, delete, desc

from model.orderlist import Orderlist

class OrderlistService (orderlist_pb2_grpc.OrderlistServiceServicer):
    def create (self, request, context):
        try:
            with engine.connect() as db:
                db.begin()
                response = db.execute(
                    insert(Orderlist).values(
                        quantity = request.quantity,
                        price_count = request.price_count,
                        orderId = request.orderId,
                        productId = request.productId,
                    )
                )
                db.commit()

                if response is None:
                    context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                    return orderlist_pb2.OrderlistCreateRes(
                        orderlist = None,
                        msg = "Gagal Menambahkan Orderlist"
                    )
                    
                return orderlist_pb2.OrderlistCreateRes(
                    orderlist = orderlist_pb2.Orderlist(
                        quantity = request.quantity,
                        price_count = request.price_count,
                        orderId = request.orderId,
                        productId = request.productId,
                        id = response.inserted_primary_key_rows[0][0],
                    ),
                    msg = "Berhasil Menambahkan Orderlist"
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
                    select(Orderlist).order_by(desc(Orderlist.id))
                )
                orderlist = []
                
                for row in response:
                    orderlist.append(
                        orderlist_pb2.Orderlist(
                            id = row[0],
                            quantity = row[1],
                            price_count = row[2],
                            orderId = row[3],
                            productId = row[4],
                        )
                    )
                return orderlist_pb2.OrderlistAllRes(
                    orderlist = orderlist,
                    msg = "Berhasil Mendapatkan Daftar Orderlist"
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
                    select(Orderlist).where(Orderlist.id == request.id)
                ).first()
                
                conn.commit()

                if response is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    return orderlist_pb2.OrderlistOneRes(
                        orderlist = None,
                    )

                return orderlist_pb2.OrderlistOneRes(
                    orderlist = orderlist_pb2.Orderlist(
                        id = response[0],
                        quantity = response[1],
                        price_count = response[2],
                        orderId = response[3],
                        productId = response[4],
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
                    update(Orderlist)
                    .where(Orderlist.id == request.id)
                    .values(
                        quantity = request.quantity,
                        price_count = request.price_count,
                        orderId = request.orderId,
                        productId = request.productId,
                    )
                )
                db.commit()

                if response is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    return orderlist_pb2.OrderlistUpdateRes(
                        orderlist = None,
                        msg = "Gagal Memperbaharui Orderlist"
                    )

                return orderlist_pb2.OrderlistUpdateRes(
                    orderlist = orderlist_pb2.Orderlist(
                        id = request.id,
                        quantity = request.quantity,
                        price_count = request.price_count,
                        orderId = request.orderId,
                        productId = request.productId,
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
                    delete(Orderlist).where(Orderlist.id == request.id)
                )
                db.commit()

                if response is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    return orderlist_pb2.OrderlistDeleteRes(msg = "Gagal Menghapus Orderlist")

                return orderlist_pb2.OrderlistDeleteRes(msg = "Berhasil Menghapus Orderlist")
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            context.set_code(grpc.StatusCode.UNKNOWN)
            return

def serve ():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    orderlist_pb2_grpc.add_OrderlistServiceServicer_to_server(OrderlistService(), server)
    server.add_insecure_port("localhost:5008")
    server.start()
    print("Server started, listening on 5008")
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    serve()
    