import grpc
import orderlist_pb2 as orderlist_pb2
import orderlist_pb2_grpc as orderlist_pb2_grpc

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
        
        return [
            dict(
                id = orderlist.id,
                quantity = orderlist.quantity,
                price_count = orderlist.price_count,
                orderId = orderlist.orderId,
                productId = orderlist.productId,
            )
            for orderlist in response.orderlist
        ]
    
    def getOne (self, id):
        response = self.stub.readOne(
            orderlist_pb2.OrderlistOneReq(id = int(id))
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
        
        return dict(
            id = response.orderlist.id,
            quantity = response.orderlist.quantity,
            price_count = response.orderlist.price_count,
            orderId = response.orderlist.orderId,
            productId = response.orderlist.productId,
        )
    
    def delete (self, id):
        response = self.stub.delete(orderlist_pb2.OrderlistDeleteReq(id = id))
        
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
            item = OrderlistClient().readAll()
            print(item)
        elif choice == 2:
            id = int(input("Enter item id: "))
            item = OrderlistClient().getOne(int(id))
            print(item)
        elif choice == 3:
            quantity = int(input("Enter item quantity: "))
            price_count = int(input("Enter item price_count: "))
            orderId = int(input("Enter item orderId: "))
            productId = int(input("Enter item productId: "))
            item = OrderlistClient().create(quantity, price_count, orderId, productId)
            print(item)
        elif choice == 4:
            id = int(input("Enter item id: "))
            quantity = int(input("Enter item quantity: "))
            price_count = int(input("Enter item price_count: "))
            orderId = int(input("Enter item orderId: "))
            productId = int(input("Enter item productId: "))
            item = OrderlistClient().update(id, quantity, price_count, orderId, productId)
            print(item)
        elif choice == 5:
            id = int(input("Enter item id: "))
            item = OrderlistClient().delete(id)
            print(item)
        elif choice == 6:
            break