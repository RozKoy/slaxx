import grpc
import product_pb2 as product_pb2
import product_pb2_grpc as product_pb2_grpc

class ProductClient:
    def __init__ (self):
        self.host = "localhost"
        self.server_port = 5005

        self.channel = grpc.insecure_channel(f"{self.host}:{self.server_port}")
        self.stub = product_pb2_grpc.ProductServiceStub(self.channel)
    
    def create (self, name, image, price, stock):
        response = self.stub.create(
            product_pb2.ProductCreateReq(
                name = name,
                image = image,
                price = price,
                stock = stock,
            )
        )
        
        if response.product is None:
            return None
        
        return dict(
            id = response.product.id,
            name = response.product.name,
            image = response.product.image,
            price = response.product.price,
            stock = response.product.stock,
        )
    
    def readAll (self):
        response = self.stub.readAll(product_pb2.ProductAllReq())
        
        if len(response.product) == 0:
            return None
        
        return [
            dict(
                id = product.id,
                name = product.name,
                image = product.image,
                price = product.price,
                stock = product.stock,
            )
            for product in response.product
        ]
    
    def one_product (self, id):
        response = self.stub.readOne(
            product_pb2.ProductOneReq(id = int(id))
        )
        
        if response.product is None:
            return None
        
        return dict(
            id = response.product.id,
            name = response.product.name,
            image = response.product.image,
            price = response.product.price,
            stock = response.product.stock,
        )
    
    def update (self, id, name, image, price, stock):
        response = self.stub.update(
            product_pb2.ProductUpdateReq(
                id = id,
                name = name,
                image = image,
                price = price,
                stock = stock,
            )
        )
        
        if response.product is None:
            return None
        
        return dict(
            id = response.product.id,
            name = response.product.name,
            image = response.product.image,
            price = response.product.price,
            stock = response.product.stock,
        )
    
    def delete (self, id):
        response = self.stub.delete(product_pb2.ProductDeleteReq(id = id))
        
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
            item = ProductClient().readAll()
            print(item)
        elif choice == 2:
            id = int(input("Enter item id: "))
            item = ProductClient().one_product(int(id))
            print(item)
        elif choice == 3:
            name = input("Enter item name: ")
            image = input("Enter item image: ")
            price = int(input("Enter item price: "))
            stock = int(input("Enter item stock: "))
            item = ProductClient().create(name, image, price, stock)
            print(item)
        elif choice == 4:
            id = int(input("Enter item id: "))
            name = input("Enter item name: ")
            image = input("Enter item image: ")
            price = int(input("Enter item price: "))
            stock = int(input("Enter item stock: "))
            item = ProductClient().update(id, name, image, price, stock)
            print(item)
        elif choice == 5:
            id = int(input("Enter item id: "))
            item = ProductClient().delete(id)
            print(item)
        elif choice == 6:
            break