from . import session

class bm_api(object):
	server = "https://api.battlemetrics.com"

	def __init__(self, token):
		self.token = token
		self.headers = {"Accept": "application/json", "Authorization": "Bearer {token}".format(token=self.token)}

	def get_server_info(self, id):
		path = "{server}/servers/{id}".format(server=self.server, id=id)
		response = session.get(path, headers=self.headers)

		return response.json()