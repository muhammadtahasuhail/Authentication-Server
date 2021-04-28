class Client:

	def __init__(self):
	
		self.hostname = '127.0.0.1'  # The server's hostname or IP address
		self.port = 9999             # The port used by the server
		self.credentials = {}
		
	def set_credentials(self, username, password):
	
		self.credentials['username'] = username
		self.credentials['password'] = password
                
	def register_credentials(self, username, password, confirmPassword):
	
		self.credentials['username'] = username
		self.credentials['password'] = password
		self.credentials['confirmPassword'] = confirmPassword
		
	def get_credentials(self):
		return self.credentials
		
	def get_server_info(self):
		return self.hostname, self.port