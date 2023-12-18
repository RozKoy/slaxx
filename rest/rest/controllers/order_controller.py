import grpc
from pyramid.response import Response
from pyramid.view import view_config, view_defaults

from rest.grpc_client.order.client import OrderClient

@view_defaults(route_name="order", renderer="json")
class OrderController:
    def __init__(self, request):
        self.request = request

    @view_config(request_method="GET")
    def get(self):
        try:
            if self.request.params.get("id") is not None:
                id = self.request.params.get("id")
                order = OrderClient().getOne(int(id))

                if order == None:
                    return Response(
                        status=404,
                        json_body={"message": "Order not found"},
                    )
                return order

            orders = OrderClient().readAll()
            return orders

        except grpc.RpcError as e:
            return Response(
                status=e.code(),
                json_body={"message": e.details()},
            )

    @view_config(request_method="POST")
    def create(self):
        try:
            if (
                "status" not in self.request.json_body
                or "item_count" not in self.request.json_body
                or "price_count" not in self.request.json_body
                or "customerId" not in self.request.json_body
            ):
                return Response(
                    status=400,
                    json_body={"message": "Required field: item_count, price_count and customerId"},
                )

            status = self.request.json_body["status"]
            item_count = int(self.request.json_body["item_count"])
            price_count = int(self.request.json_body["price_count"])
            customerId = self.request.json_body["customerId"]

            order = OrderClient()
            result = order.create(
                status, item_count, price_count, customerId
            )
            
            if result == None:
                return Response(
                    status=400,
                    json_body={"message": "Failed to create order"},
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
            old_order = OrderClient().getOne(id)

            status = self.request.json_body["status"]
            if status is None:
                status = old_product.status
            item_count = int(self.request.json_body["item_count"])
            if item_count is None:
                item_count = old_product.item_count
            price_count = int(self.request.json_body["price_count"])
            if price_count is None:
                price_count = old_product.price_count
            customerId = self.request.json_body["customerId"]
            if customerId is None:
                customerId = old_product.customerId
                
            order = OrderClient()
            result = order.update(
                id, status, item_count, price_count, customerId
            )
            
            if result == None:
                return Response(
                    status=400,
                    json_body={"message": "Failed to update order"},
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
                
            order = OrderClient()
            result = order.delete(int(self.request.params.get("id")))
            
            if result == None:
                return Response(
                    status=400,
                    json_body={"message": "Failed to delete order"},
                )

            return result
        except grpc.RpcError as e:
            return Response(
                status=e.code(),
                json_body={"message": e.details()},
            )
