import uuid

class OrderRequest:
	

	def __init__(
		self, foodorder, description, quantity, username, requestId = str(
			uuid.uuid4())):
		self.requestId = requestId
		self.foodorder = foodorder
		self.description = description
		self.quantity = quantity
		self.owner = username

	def getDictionary(self):
		return 	{
		'id': self.requestId,
		'food order': self.foodorder,
		'description': self.description,
		'quantity': self.quantity,
		'owner': self.owner
		}

	def getOwner(self):
		return self.owner

	def getOrderId(self):
		return self.requestId
