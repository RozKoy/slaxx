import grpc
import rest.grpc_client.product.product_pb2 as product_pb2
import rest.grpc_client.product.product_pb2_grpc as product_pb2_grpc

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