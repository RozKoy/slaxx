import grpc
from pyramid.response import Response
from pyramid.view import view_config, view_defaults

from rest.grpc_client.product.client import ProductClient

@view_defaults(route_name="product", renderer="json")
class ProductController:
    def __init__(self, request):
        self.request = request

    @view_config(request_method="GET")
    def get(self):
        try:
            if self.request.params.get("id") is not None:
                id = self.request.params.get("id")
                product = ProductClient().one_product(int(id))

                if product == None:
                    return Response(
                        status=404,
                        json_body={"message": "Order not found"},
                    )
                return product

            products = ProductClient().readAll()
            return products

        except grpc.RpcError as e:
            return Response(
                status=e.code(),
                json_body={"message": e.details()},
            )

    @view_config(request_method="POST")
    def create(self):
        try:
            if (
                "name" not in self.request.json_body
                or "image" not in self.request.json_body
                or "price" not in self.request.json_body
                or "stock" not in self.request.json_body
            ):
                return Response(
                    status=400,
                    json_body={"message": "Required field: name, image, price and stock"},
                )

            name = self.request.json_body["name"]
            image = self.request.json_body["image"]
            price = int(self.request.json_body["price"])
            stock = int(self.request.json_body["stock"])

            product = ProductClient()
            result = product.create(
                name, image, price, stock
            )
            
            if result == None:
                return Response(
                    status=400,
                    json_body={"message": "Failed to create product"},
                )

            return result
        except grpc.RpcError as e:
            return Response(
                status=e.code(),
                json_body={"message": e.details()},
            )
    
    @view_config(request_method="PUT")
    def update(self):
        try:
            if (
                "id" not in self.request.json_body
            ):
                return Response(
                    status=400,
                    json_body={"message": "Required field: id"},
                )

            id = int(self.request.json_body["id"])
            old_product = ProductClient().one_product(id)

            name = self.request.json_body["name"]
            if name is None:
                name = old_product.name
            image = self.request.json_body["image"]
            if image is None:
                image = old_product.image
            price = int(self.request.json_body["price"])
            if price is None:
                price = old_product.price
            stock = int(self.request.json_body["stock"])
            if stock is None:
                stock = old_product.stock
                
            product = ProductClient()
            result = product.update(
                id, name, image, price, stock
            )
            
            if result == None:
                return Response(
                    status=400,
                    json_body={"message": "Failed to update product"},
                )

            return result
        except grpc.RpcError as e:
            return Response(
                status=e.code(),
                json_body={"message": e.details()},
            )
    
    @view_config(request_method="DELETE")
    def delete(self):
        try:
            if self.request.params.get("id") is None:
                return Response(
                    status=400,
                    json_body={"message": "Required field: id"},
                )
                
            product = ProductClient()
            result = product.delete(int(self.request.params.get("id")))
            
            if result == None:
                return Response(
                    status=400,
                    json_body={"message": "Failed to delete product"},
                )

            return result
        except grpc.RpcError as e:
            return Response(
                status=e.code(),
                json_body={"message": e.details()},
            )
