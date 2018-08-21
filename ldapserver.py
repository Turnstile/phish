from ldap3 import Connection, Server, MODIFY_REPLACE 

class LDAPServer:
	
	def __init__(self, server, username, password):
		self.server = server
		self.username = username
		self.password = password
		self.conn = self.open_connection(server)

	#open connection
	def open_connection(self, server):
		return Connection(server, self.username, self.password, auto_bind=True)	

	def get_user(self, dn):
		self.conn.search(dn, '(objectclass=person)', attributes=['loginDisabled', 'givenName', 'sn', 'telephoneNumber'])

	def disable_user(self, dn):
		self.conn.modify(dn, {'loginDisabled':[(MODIFY_REPLACE, ['TRUE'])]}) 

	def enable_user(self, dn):
		self.conn.modify(dn, {'loginDisabled':[(MODIFY_REPLACE, ['FALSE'])]}) 

	def close_connection(self):
		self.conn.unbind()
