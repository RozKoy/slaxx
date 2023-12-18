import grpc
import time
import rest.grpc_client.order.order_pb2 as order_pb2
import rest.grpc_client.order.order_pb2_grpc as order_pb2_grpc

from rest.grpc_client.user.client import UserClient

class OrderClient:
    def __init__ (self):
        self.host = "localhost"
        self.server_port = 5007

        self.channel = grpc.insecure_channel(f"{self.host}:{self.server_port}")
        self.stub = order_pb2_grpc.OrderServiceStub(self.channel)
    
    def create (self, status, item_count, price_count, customerId):
        timestamp = time.time()
        create_at = time.ctime(timestamp)
        response = self.stub.create(
            order_pb2.OrderCreateReq(
                status = status,
                item_count = item_count,
                price_count = price_count,
                create_at = create_at,
                customerId = customerId,
            )
        )
        
        if response.order is None:
            return None
        
        return dict(
            id = response.order.id,
            status = response.order.status,
            create_at = response.order.create_at,
            item_count = response.order.item_count,
            customerId = response.order.customerId,
            price_count = response.order.price_count,
        )
    
    def readAll (self):
        response = self.stub.readAll(order_pb2.OrderAllReq())
        
        if len(response.order) == 0:
            return None
        
        customer = UserClient()

        return [
            dict(
                id = order.id,
                status = order.status,
                create_at = order.create_at,
                customerId = order.customerId,
                item_count = order.item_count,
                price_count = order.price_count,
                customer = customer.one_user(order.customerId),
            )
            for order in response.order
        ]
    
    def getOne (self, id):
        response = self.stub.readOne(
            order_pb2.OrderOneReq(id = int(id))
        )
        
        if response.order is None:
            return None

        customer = UserClient().one_user(response.order.customerId)
        
        return dict(
            id = response.order.id,
            customer = customer,
            status = response.order.status,
            create_at = response.order.create_at,
            item_count = response.order.item_count,
            customerId = response.order.customerId,
            price_count = response.order.price_count,
        )
    
    def update (self, id, status, item_count, price_count, customerId):
        response = self.stub.update(
            order_pb2.OrderUpdateReq(
                id = id,
                status = status,
                item_count = item_count,
                price_count = price_count,
                customerId = customerId,
            )
        )
        
        if response.order is None:
            return None
        
        return dict(
            id = response.order.id,
            status = response.order.status,
            create_at = response.order.create_at,
            item_count = response.order.item_count,
            customerId = response.order.customerId,
            price_count = response.order.price_count,
        )
    
    def delete (self, id):
        response = self.stub.delete(order_pb2.OrderDeleteReq(id = id))
        
        if response is None:
            return None
        
        return dict(
            message = response.msg
        )