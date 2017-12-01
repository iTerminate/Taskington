import sys
import threading

sys.path.append('/local/djarosz/development/Taskington/project/')

import sqlalchemy
from sqlalchemy.orm import sessionmaker

class Db:
	__instance = None
	__lock = threading.RLock()

	def __init__(self):
		Db.__lock.acquire()
		try:
			if Db.__instance is not None:
				raise Db.__instance
			Db.__instance = self
			self.engine = sqlalchemy.create_engine('postgresql://taskington@localhost/taskington', echo=True)
			self.dbConnection = self.engine.connect()

			Session = sessionmaker(bind=self.engine)
			self.session = Session()
		finally:
			Db.__lock.release()

	@classmethod
	def getInstance(cls):
		if cls.__instance is None:
			cls.__instance = Db()
		return cls.__instance



if __name__ == "__main__":
	db = Db()
	db1 = Db()
	db1 = Db()
	db1 = Db()
	db1 = Db()
	db1 = Db()
	db1 = Db()
	db1 = Db()








