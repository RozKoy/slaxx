import grpc
from pyramid.response import Response
from pyramid.view import view_config, view_defaults

from rest.grpc_client.orderlist.client import OrderlistClient

@view_defaults(route_name="orderlist", renderer="json")
class OrderlistController:
    def __init__(self, request):
        self.request = request

    @view_config(request_method="GET")
    def get(self):
        try:
            if self.request.params.get("id") is not None:
                id = self.request.params.get("id")
                orderlist = OrderlistClient().getOne(int(id))

                if orderlist == None:
                    return Response(
                        status=404,
                        json_body={"message": "Order not found"},
                    )
                return orderlist

            orderlists = OrderlistClient().readAll()
            return orderlists

        except grpc.RpcError as e:
            return Response(
                status=e.code(),
                json_body={"message": e.details()},
            )

    @view_config(request_method="POST")
    def create(self):
        try:
            if (
                "quantity" not in self.request.json_body
                or "price_count" not in self.request.json_body
                or "orderId" not in self.request.json_body
                or "productId" not in self.request.json_body
            ):
                return Response(
                    status=400,
                    json_body={"message": "Required field: quantity, price_count, orderId and productId"},
                )

            quantity = int(self.request.json_body["quantity"])
            price_count = int(self.request.json_body["price_count"])
            orderId = int(self.request.json_body["orderId"])
            productId = int(self.request.json_body["productId"])

            orderlist = OrderlistClient()
            result = orderlist.create(
                quantity, price_count, orderId, productId
            )
            
            if result == None:
                return Response(
                    status=400,
                    json_body={"message": "Failed to create orderlist"},
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
            old_orderlist = OrderlistClient().getOne(id)

            quantity = int(self.request.json_body["quantity"])
            if quantity is None:
                quantity = old_product.quantity
            price_count = int(self.request.json_body["price_count"])
            if price_count is None:
                price_count = old_product.price_count
            orderId = int(self.request.json_body["orderId"])
            if orderId is None:
                orderId = old_product.orderId
            productId = int(self.request.json_body["productId"])
            if productId is None:
                productId = old_product.productId
                
            orderlist = OrderlistClient()
            result = orderlist.update(
                id, quantity, price_count, orderId, productId
            )
            
            if result == None:
                return Response(
                    status=400,
                    json_body={"message": "Failed to update orderlist"},
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
                
            orderlist = OrderlistClient()
            result = orderlist.delete(int(self.request.params.get("id")))
            
            if result == None:
                return Response(
                    status=400,
                    json_body={"message": "Failed to delete orderlist"},
                )

            return result
        except grpc.RpcError as e:
            return Response(
                status=e.code(),
                json_body={"message": e.details()},
            )
