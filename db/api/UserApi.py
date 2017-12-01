from api.BaseApi import BaseApi
from common.Mapping import Role, User, Beamline


class UserApi(BaseApi):

	def __init__(self):
		BaseApi.__init__(self)

	def __createRole(self, name, description=None):
		return self._createNameDescriptionEntity(Role, name, description)

	def __createUser(self, username, local_password, role=None):
		user = User()
		user.username = username
		user.local_password = local_password
		if role is not None:
			user.roles = [role]
		return user

	def __createBeamline(self, name, description=None):
		return self._createNameDescriptionEntity(Beamline, name, description)

	def __getRoleCreateIfNeeded(self, roleName):
		try:
			return self._findDbObjectByName(Role, roleName)
		except Exception, ex:
			return self.__createRole(roleName)

	def __getBeamlineCreateIfNeeded(self, beamlineName):
		try:
			return self._findDbObjectByName(Beamline, beamlineName)
		except Exception, ex:
			return self.__createBeamline(beamlineName)

	def getUserByUsername(self, username):
		return self._findDbObjectByAttribute(User, 'username', username)

	def getUsers(self):
		return self._findAllDbObjects(User)

	def getBeamlines(self):
		return self._findAllDbObjects(Beamline)

	def getRoles(self):
		return self._findAllDbObjects(Role)

	def addBeamline(self, name, description=None):
		beamline = self.__createBeamline(name, description)

		self.session.add(beamline)
		self.session.commit()

		return beamline

	def assignUserRoles(self, username, roleNames, clear=False):
		user = self.getUserByUsername(username)
		user.roles = []

		for roleName in roleNames:
			dbRole = self.__getRoleCreateIfNeeded(roleName)
			user.roles.append(dbRole)
			self.session.add(dbRole)

		self.session.add(user)
		self.session.commit()

		return user

	def assignUserBeamline(self, username, beamlineNames):
		user = self.getUserByUsername(username)
		user.beamlines = []

		for beamlineName in beamlineNames:
			dbBeamline = self.__getBeamlineCreateIfNeeded(beamlineName)
			user.beamlines.append(dbBeamline)
			self.session.add(dbBeamline)

		self.session.add(user)
		self.session.commit()

		return user

	def addUser(self, username, local_password=None, roleName=None):
		role = None
		if roleName is not None:
			role = self.__getRoleCreateIfNeeded(roleName)
			self.session.add(role)

		user = self.__createUser(username, local_password, role)

		self.session.add(user)
		self.session.commit()

		return user

	def addRole(self, name, description=None):
		role = self.__createRole(name, description)

		self.session.add(role)
		self.session.commit()

		return role