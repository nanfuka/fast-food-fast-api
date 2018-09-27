import uuid


class OrderRequest:

    def __init__(
            self, food_order, description, quantity, username, request_Id=str(
                uuid.uuid4())):
        self.request_Id = request_Id
        self.food_order = food_order
        self.description = description
        self.quantity = quantity
        self.owner = username

    def get_dictionary(self):
        return {
            'id': self.request_Id,
            'food_order': self.food_order,
            'description': self.description,
            'quantity': self.quantity,
            'owner': self.owner
        }

    def get_owner(self):
        return self.owner

    def get_order_Id(self):
        return self.request_Id
