from api.BaseApi import BaseApi
from common.Mapping import Software, ArgumentType, SoftwareArg


class SoftwareApi(BaseApi):

	def __init__(self):
		BaseApi.__init__(self)

	def __createSoftware(self, name, description=None):
		return self._createNameDescriptionEntity(Software, name, description)

	def __createArgumentType(self, type, description=None):
		return self._createNameDescriptionEntity(ArgumentType, type, description, nameAttribute='type')

	def __createSoftwareArg(self, softwareName, argumentTypeName, key):
		software = self.getSoftwareByName(softwareName)
		argumentType = self.getArgumentTypeByName(argumentTypeName)

		softwareArg = SoftwareArg()
		softwareArg.software = software
		softwareArg.argument_type = argumentType
		softwareArg.key = key

		return softwareArg

	def getArgumentTypeByName(self, argumentTypeName):
		return self._findDbObjectByAttribute(ArgumentType, "type", argumentTypeName)

	def getSoftwareByName(self, name):
		return self._findDbObjectByName(Software, name)

	def getSoftware(self):
		return self._findAllDbObjects(Software)

	def addSoftware(self, name, description=None):
		software = self.__createSoftware(name, description)

		self.session.add(software)
		self.session.commit()

		return software

	def addArgumentType(self, type, description=None):
		argumentType = self.__createArgumentType(type, description)

		self.session.add(argumentType)
		self.session.commit()

		return argumentType

	def addSoftwareArg(self, softwareName, argumentTypeName, key):
		softwareArg = self.__createSoftwareArg(softwareName, argumentTypeName, key)

		self.session.add(softwareArg)
		self.session.commit()

		return softwareArg

	def getSoftwareArg(self, softwareName, key):
		software = self.getSoftwareByName(softwareName)
		softwareArg = self.session.query(SoftwareArg)\
			.filter(SoftwareArg.software_id == software['id'])\
			.filter(SoftwareArg.key == key).one()

		return softwareArg

