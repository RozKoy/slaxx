import time
import grpc
import logging
import traceback
import product_pb2
import product_pb2_grpc
from concurrent import futures
from database.config import engine
from sqlalchemy import insert, text, values, select, update, delete, desc

from model.product import Product

class ProductService (product_pb2_grpc.ProductServiceServicer):
    def create (self, request, context):
        try:
            with engine.connect() as db:
                db.begin()
                response = db.execute(
                    insert(Product).values(
                        name = request.name, 
                        image = request.image,
                        price = request.price,
                        stock = request.stock
                    )
                )
                db.commit()

                if response is None:
                    context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                    return product_pb2.ProductCreateRes(
                        product = None,
                        msg = "Gagal Menambahkan Produk"
                    )
                    
                return product_pb2.ProductCreateRes(
                    product = product_pb2.Product(
                        name = request.name,
                        image = request.image,
                        price = request.price,
                        stock = request.stock,
                        id = response.inserted_primary_key_rows[0][0],
                    ),
                    msg = "Berhasil Menambahkan Produk"
                )
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            context.set_code(grpc.StatusCode.UNKNOWN)
            return

    def readAll (self, request, context):
        try:
            with engine.connect() as db:
                response = conn.execute(
                    select(Product).order_by(desc(Product.id))
                )
                print(response)
                return None

                # products = [
                #     product_pb2.Product(
                #         id = product.id,
                #         name = product.name,
                #         image = product.image,
                #         price = product.price,
                #         stock = product.stock,
                #     )
                #     for product in response.product
                # ]

                # return product_pb2.ProductAllRes(
                #     product = products,
                #     msg = "Berhasil Mendapatkan Daftar Produk"
                # )
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            context.set_code(grpc.StatusCode.UNKNOWN)
            return

    def readOne (self, request, context):
        try:
            with engine.connect() as conn:
                response = conn.execute(
                    select(Product).where(Product.id == request.id)
                ).first()
                conn.commit()

                if response is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    return product_pb2.ProductOneRes(
                        product = None,
                        msg = "Gagal Mendapatkan Produk"
                    )

                return product_pb2.ProductOneRes(
                    product = product_pb2.Product(
                        id = response[0],
                        price = response[1],
                        stock = response[2],
                        name = response[3],
                        image = response[4],
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
                    update(Product)
                    .where(Product.id == request.id)
                    .values(
                        name = request.name,
                        image = request.image,
                        price = request.price,
                        stock = request.stock,
                    )
                )
                db.commit()

                if response is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    return product_pb2.ProductUpdateRes(
                        product = None,
                        msg = "Gagal Memperbaharui Produk"
                    )

                return product_pb2.ProductUpdateRes(
                    product = product_pb2.Product(
                        id = request.id,
                        name = request.name,
                        image = request.image,
                        price = request.price,
                        stock = request.stock,
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
                    delete(Product).where(Product.id == request.id)
                )
                db.commit()

                if response is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    return product_pb2.ProductDeleteRes(msg = "Gagal Menghapus Produk")

                return product_pb2.ProductDeleteRes(msg = "Berhasil Menghapus Produk")
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            context.set_code(grpc.StatusCode.UNKNOWN)
            return

def serve ():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    product_pb2_grpc.add_ProductServiceServicer_to_server(ProductService(), server)
    server.add_insecure_port("localhost:5005")
    server.start()
    print("Server started, listening on 5005")
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    serve()
    