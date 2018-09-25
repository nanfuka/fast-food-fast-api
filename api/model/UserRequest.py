import uuid

class UserRequest:
	def __init__(self,requestTitle,requestType,requestCategory,requestStatus,username,requestId= str(uuid.uuid4())):
		self.requestId=requestId
		self.requestTitle=requestTitle
		self.requestType=requestType
		self.requestCategory=requestCategory
		self.requestStatus=requestStatus
		self.owner=username

	def getDictionary(self):
		return 	{
		'id' : self.requestId,
		'title' : self.requestTitle,
		'type' : self.requestType,
		'category' : self.requestCategory,
		'status' : self.requestStatus,
		'owner' : self.owner
		}
	def getOwner(self):
		return self.owner

	def getId(self):
		return self.requestId





	
