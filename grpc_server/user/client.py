import grpc
import user_pb2 as user_pb2
import user_pb2_grpc as user_pb2_grpc

class UserClient:
    def __init__ (self):
        self.host = "localhost"
        self.server_port = 5006

        self.channel = grpc.insecure_channel(f"{self.host}:{self.server_port}")
        self.stub = user_pb2_grpc.UserServiceStub(self.channel)
    
    def create (self, role, name, email, address, password, phone_number):
        response = self.stub.create(
            user_pb2.UserCreateReq(
                role = bool(role),
                name = name,
                email = email,
                address = address,
                password = password,
                phone_number = phone_number
            )
        )
        
        if response.user is None:
            return None
        
        return dict(
            id = response.user.id,
            role = response.user.role,
            name = response.user.name,
            email = response.user.email,
            address = response.user.address,
            password = response.user.password,
            phone_number = response.user.phone_number,
        )
    
    def readAll (self):
        response = self.stub.readAll(user_pb2.UserAllReq())
        
        if len(response.user) == 0:
            return None
        
        return [
            dict(
                id = user.id,
                role = user.role,
                name = user.name,
                email = user.email,
                address = user.address,
                password = user.password,
                phone_number = user.phone_number,
            )
            for user in response.user
        ]
    
    def one_user (self, id):
        response = self.stub.readOne(
            user_pb2.UserOneReq(id = int(id))
        )
        
        if response.user is None:
            return None
        
        return dict(
            id = response.user.id,
            role = response.user.role,
            name = response.user.name,
            email = response.user.email,
            address = response.user.address,
            password = response.user.password,
            phone_number = response.user.phone_number,
        )
    
    def update (self, id, role, name, email, address, password, phone_number):
        response = self.stub.update(
            user_pb2.UserUpdateReq(
                id = id,
                role = bool(role),
                name = name,
                email = email,
                address = address,
                password = password,
                phone_number = phone_number
            )
        )
        
        if response.user is None:
            return None
        
        return dict(
            id = response.user.id,
            role = response.user.role,
            name = response.user.name,
            email = response.user.email,
            address = response.user.address,
            password = response.user.password,
            phone_number = response.user.phone_number,
        )
    
    def delete (self, id):
        response = self.stub.delete(user_pb2.UserDeleteReq(id = id))
        
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
            item = UserClient().readAll()
            print(item)
        elif choice == 2:
            id = int(input("Enter item id: "))
            item = UserClient().one_user(int(id))
            print(item)
        elif choice == 3:
            role = int(input("Enter item role: "))
            name = input("Enter item name: ")
            email = input("Enter item email: ")
            address = input("Enter item address: ")
            password = input("Enter item password: ")
            phone_number = input("Enter item phone_number: ")
            item = UserClient().create(role, name, email, address, password, phone_number)
            print(item)
        elif choice == 4:
            id = int(input("Enter item id: "))
            role = int(input("Enter item role: "))
            name = input("Enter item name: ")
            email = input("Enter item email: ")
            address = input("Enter item address: ")
            password = input("Enter item password: ")
            phone_number = input("Enter item phone_number: ")
            item = UserClient().update(id, role, name, email, address, password, phone_number)
            print(item)
        elif choice == 5:
            id = int(input("Enter item id: "))
            item = UserClient().delete(id)
            print(item)
        elif choice == 6:
            break