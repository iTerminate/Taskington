from common.Db import Db
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm.exc import NoResultFound


class BaseApi:

	def __init__(self):
		self.db = Db.getInstance()
		self.session = self.db.session

	def _findDbObjectByAttribute(self, entityDbObject, attributeKey, attributeValue):
		try:
			dbObject = self.session.query(entityDbObject).filter(getattr(entityDbObject, attributeKey)==attributeValue).one()
			return dbObject
		except NoResultFound, ex:
			raise ex

	def _findDbObjectByName(self, entityDbObject, name):
		return self._findDbObjectByAttribute(entityDbObject, 'name', name)

	def _findAllDbObjects(self, entityDbObject):
		return self.session.query(entityDbObject).all()

	def _createNameDescriptionEntity(self, entityDbObject, name, description, nameAttribute = 'name'):
		entityInstance = entityDbObject()
		setattr(entityInstance, nameAttribute, name)
		entityInstance.description = description
		return entityInstance

	def listObjectToDict(self, objectList):
		newList = []

		for object in objectList:
			newList.append(self.objectToDict(object))

		return newList

	def objectToDict(self, object):
		mapper = class_mapper(object.__class__)

		dictObject = {}
		for column in mapper.columns:
			dictObject[self.toCamelcase(column.key)] = str(getattr(object, column.key))

		return dictObject

	def toCamelcase(self, underscoreStr):
		res = ""
		for word in underscoreStr.split("_"):
			res += word[0].upper() + word[1:]
		return res