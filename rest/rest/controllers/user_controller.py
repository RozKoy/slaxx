import grpc
from pyramid.response import Response
from pyramid.view import view_config, view_defaults

from rest.grpc_client.user.client import UserClient

@view_defaults(route_name="user", renderer="json")
class UserController:
    def __init__(self, request):
        self.request = request

    @view_config(request_method="GET")
    def get(self):
        try:
            if self.request.params.get("id") is not None:
                id = self.request.params.get("id")
                user = UserClient().one_user(int(id))

                if user == None:
                    return Response(
                        status=404,
                        json_body={"message": "Order not found"},
                    )
                return user

            users = UserClient().readAll()
            return users

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
                or "email" not in self.request.json_body
                or "password" not in self.request.json_body
            ):
                return Response(
                    status=400,
                    json_body={"message": "Required field: name, email and password"},
                )

            role = 0
            name = self.request.json_body["name"]
            email = self.request.json_body["email"]
            address = self.request.json_body["address"]
            password = self.request.json_body["password"]
            phone_number = self.request.json_body["phone_number"]

            user = UserClient()
            result = user.create(
                role, name, email, address, password, phone_number
            )
            
            if result == None:
                return Response(
                    status=400,
                    json_body={"message": "Failed to create user"},
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
            old_user = UserClient().one_user(id)

            role = 0
            name = self.request.json_body["name"]
            if name is None:
                name = old_user.name
            email = self.request.json_body["email"]
            if email is None:
                email = old_user.email
            address = self.request.json_body["address"]
            if address is None:
                address = old_user.address
            password = self.request.json_body["password"]
            if password is None:
                password = old_user.password
            phone_number = self.request.json_body["phone_number"]
            if phone_number is None:
                phone_number = old_user.phone_number
                
            user = UserClient()
            result = user.update(
                id, role, name, email, address, password, phone_number
            )
            
            if result == None:
                return Response(
                    status=400,
                    json_body={"message": "Failed to update user"},
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
                
            user = UserClient()
            result = user.delete(int(self.request.params.get("id")))
            
            if result == None:
                return Response(
                    status=400,
                    json_body={"message": "Failed to delete user"},
                )

            return result
        except grpc.RpcError as e:
            return Response(
                status=e.code(),
                json_body={"message": e.details()},
            )
