import grpc
import rest.grpc_client.orderlist.orderlist_pb2 as orderlist_pb2
import rest.grpc_client.orderlist.orderlist_pb2_grpc as orderlist_pb2_grpc

from rest.grpc_client.order.client import OrderClient
from rest.grpc_client.product.client import ProductClient

class OrderlistClient:
    def __init__ (self):
        self.host = "localhost"
        self.server_port = 5008

        self.channel = grpc.insecure_channel(f"{self.host}:{self.server_port}")
        self.stub = orderlist_pb2_grpc.OrderlistServiceStub(self.channel)
    
    def create (self, quantity, price_count, orderId, productId):
        response = self.stub.create(
            orderlist_pb2.OrderlistCreateReq(
                quantity = quantity,
                price_count = price_count,
                orderId = orderId,
                productId = productId
            )
        )
        
        if response.orderlist is None:
            return None
        
        return dict(
            id = response.orderlist.id,
            quantity = response.orderlist.quantity,
            price_count = response.orderlist.price_count,
            orderId = response.orderlist.orderId,
            productId = response.orderlist.productId,
        )
    
    def readAll (self):
        response = self.stub.readAll(orderlist_pb2.OrderlistAllReq())
        
        if len(response.orderlist) == 0:
            return None
        
        order = OrderClient()
        product = ProductClient()

        return [
            dict(
                id = orderlist.id,
                orderId = orderlist.orderId,
                quantity = orderlist.quantity,
                productId = orderlist.productId,
                price_count = orderlist.price_count,
                order = order.getOne(orderlist.orderId),
                product = product.one_product(orderlist.productId),
            )
            for orderlist in response.orderlist
        ]
    
    def getOne (self, id):
        response = self.stub.readOne(
            orderlist_pb2.OrderlistOneReq(id = int(id))
        )
        
        if response.orderlist is None:
            return None

        order = OrderClient().getOne(response.orderlist.orderId)
        product = ProductClient().one_product(response.orderlist.productId)
        
        return dict(
            id = response.orderlist.id,
            order = order,
            product = product,
            orderId = response.orderlist.orderId,
            quantity = response.orderlist.quantity,
            productId = response.orderlist.productId,
            price_count = response.orderlist.price_count,
        )
    
    def update (self, id, quantity, price_count, orderId, productId):
        response = self.stub.update(
            orderlist_pb2.OrderlistUpdateReq(
                id = id,
                quantity = quantity,
                price_count = price_count,
                orderId = orderId,
                productId = productId
            )
        )
        
        if response.orderlist is None:
            return None

        order = OrderClient().getOne(response.orderlist.orderId)
        product = ProductClient().one_product(response.orderlist.productId)
        
        return dict(
            id = response.orderlist.id,
            order = order,
            product = product,
            orderId = response.orderlist.orderId,
            quantity = response.orderlist.quantity,
            productId = response.orderlist.productId,
            price_count = response.orderlist.price_count,
        )
    
    def delete (self, id):
        response = self.stub.delete(orderlist_pb2.OrderlistDeleteReq(id = id))
        
        if response is None:
            return None
        
        return dict(
            message = response.msg
        )