import grpc
import time
import order_pb2 as order_pb2
import order_pb2_grpc as order_pb2_grpc

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
            item_count = response.order.item_count,
            price_count = response.order.price_count,
            create_at = response.order.create_at,
            customerId = response.order.customerId,
        )
    
    def readAll (self):
        response = self.stub.readAll(order_pb2.OrderAllReq())
        
        if len(response.order) == 0:
            return None
        
        return [
            dict(
                id = order.id,
                status = order.status,
                item_count = order.item_count,
                price_count = order.price_count,
                create_at = order.create_at,
                customerId = order.customerId,
            )
            for order in response.order
        ]
    
    def getOne (self, id):
        response = self.stub.readOne(
            order_pb2.OrderOneReq(id = int(id))
        )
        
        if response.order is None:
            return None
        
        return dict(
            id = response.order.id,
            status = response.order.status,
            item_count = response.order.item_count,
            price_count = response.order.price_count,
            create_at = response.order.create_at,
            customerId = response.order.customerId,
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
            item_count = response.order.item_count,
            price_count = response.order.price_count,
            create_at = response.order.create_at,
            customerId = response.order.customerId,
        )
    
    def delete (self, id):
        response = self.stub.delete(order_pb2.OrderDeleteReq(id = id))
        
        if response is None:
            return None
        
        return dict(
            message = response.msg
        )

if __name__ == "__main__":
    while True:
        print("1. List item")
        print("2. Get item")
        print("3. Create item")
        print("4. Update item")
        print("5. Delete item")
        print("6. Exit")
        
        choice = int(input("Enter your choice: "))

        if choice == 1:
            item = OrderClient().readAll()
            print(item)
        elif choice == 2:
            id = int(input("Enter item id: "))
            item = OrderClient().getOne(int(id))
            print(item)
        elif choice == 3:
            status = input("Enter item status: ")
            item_count = int(input("Enter item count: "))
            price_count = int(input("Enter item price: "))
            customerId = int(input("Enter item customer id: "))
            item = OrderClient().create(status, item_count, price_count, customerId)
            print(item)
        elif choice == 4:
            id = int(input("Enter item id: "))
            status = input("Enter item status: ")
            item_count = int(input("Enter item count: "))
            price_count = int(input("Enter item price: "))
            customerId = int(input("Enter item customer id: "))
            item = OrderClient().update(id, status, item_count, price_count, customerId)
            print(item)
        elif choice == 5:
            id = int(input("Enter item id: "))
            item = OrderClient().delete(id)
            print(item)
        elif choice == 6:
            break