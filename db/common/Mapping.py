from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Beamline(Base):
	__tablename__ = "beamline"

	id = Column(Integer, primary_key=True)
	name = Column(String)
	description = Column(String)

class Role(Base):
	__tablename__ = "role"

	id = Column(Integer, primary_key=True)
	name = Column(String)
	description = Column(String)

class UserBeamline(Base):
	__tablename__ = "user_beamline"

	beamline_id = Column(Integer, ForeignKey('beamline.id'), primary_key=True)
	user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)

class UserRole(Base):
	__tablename__ = "user_role"

	role_id = Column(Integer, ForeignKey('role.id'), primary_key=True)
	user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)

class User(Base):
	__tablename__ = "user"

	id = Column(Integer, primary_key=True)
	username = Column(String)
	local_password = Column(String)
	beamlines = relationship(Beamline, secondary="user_beamline")
	roles = relationship(Role, secondary="user_role")

class Software(Base):
	__tablename__ = "software"

	id = Column(Integer, primary_key=True)
	name = Column(String)
	description = Column(String)

	softwareArguments = relationship("SoftwareArg")

class ArgumentType(Base):
	__tablename__ = "argument_type"

	id = Column(Integer, primary_key=True)
	type = Column(String)
	description = Column(String)

class SoftwareArg(Base):
	__tablename__ = "software_arg"

	id = Column(Integer, primary_key=True)
	software_id = Column(Integer, ForeignKey("software.id"))
	software = relationship("Software")
	key = Column(String)
	argument_type_id = Column(Integer, ForeignKey("argument_type.id"))
	argument_type = relationship("ArgumentType")

class ProcessNode(Base):
	__tablename__ = "process_node"

	id = Column(Integer, primary_key=True)
	computer_name = Column(String)
	num_threads = Column(Integer)
	hostname = Column(String)
	port = Column(Integer)
	status = Column(Integer)
	heartbeat = Column(DateTime)
	process_cpu_percent = Column(Float)
	process_mem_percent = Column(Float)
	system_cpu_percent = Column(Float)
	system_mem_percent = Column(Float)
	system_swap_percent = Column(Float)

class Status(Base):
	__tablename__ = "status"

	id = Column(Integer, primary_key=True)
	status = Column(String)
	description = Column(String)

class JobStatus(Base):
	__tablename__ = "job_status"

	id = Column(Integer, primary_key=True)
	process_node_id = Column(Integer, ForeignKey("process_node.id"))
	process_node = relationship("ProcessNode")
	status_id = Column(Integer, ForeignKey("status.id"))
	status = relationship("Status")
	start_proc_time = Column(DateTime)
	finish_proc_time = Column(DateTime)
	log_path = Column(String)

class JobDataset(Base):
	__tablename__ = "job_dataset"

	id = Column(Integer, primary_key=True)
	dataset_path = Column(String)
	process_all = Column(Boolean)
	datasetFiles = relationship("DatasetFileToProcess")

class DatasetFileToProcess(Base):
	__tablename__ = "dataset_file_to_process"

	dataset_id = Column(Integer, ForeignKey("job_dataset.id"), primary_key=True)
	dataset = relationship("JobDataset")
	file_name = Column(String, primary_key=True)

class Job(Base):
	__tablename__ = "job"

	id = Column(Integer, primary_key=True)
	is_concurrent = Column(Boolean)
	priority = Column(Integer)
	experiment_software_id = Column(Integer, ForeignKey("software.id"))
	experiment_software = relationship("Software")
	dataset_id = Column(Integer, ForeignKey("job_dataset.id"))
	dataset = relationship("JobDataset")
	job_status_id = Column(Integer, ForeignKey("job_status.id"))
	job_status = relationship("JobStatus")
	submitted_by_user_id = Column(Integer, ForeignKey("user.id"))
	submitted_by_user = relationship("User")
	jobEmails = relationship("JobEmail")

class JobEmail(Base):
	__tablename__ = "job_email"

	job_id = Column(Integer, ForeignKey("job.id"), primary_key=True)
	job = relationship("Job")
	email = Column(String, primary_key=True)
	attachment = Column(String)

class ProcessNodeSupportedSoftware(Base):
	__tablename__ = "process_node_supported_software"

	process_node_id = Column(Integer, ForeignKey("process_node.id"), primary_key=True)
	process_node = relationship("ProcessNode")
	software_id = Column(Integer, ForeignKey("software.id"), primary_key=True)
	software = relationship("Software")



