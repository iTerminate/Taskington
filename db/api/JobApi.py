from api.BaseApi import BaseApi
from api.SoftwareApi import SoftwareApi
from api.UserApi import UserApi
from common.Mapping import JobDataset, DatasetFileToProcess, ProcessNode, Status, JobStatus, Job, JobEmail


class JobApi(BaseApi):

	def __init__(self):
		BaseApi.__init__(self)
		self.softwareApi = SoftwareApi()
		self.userApi = UserApi()

	def _createJobDataset(self, datasetPath, processAll):
		jobDataset = JobDataset()
		jobDataset.dataset_path = datasetPath
		jobDataset.process_all = processAll

		return jobDataset

	def _createDatasetFileToProcess(self, datasetDBObject, fileName):
		datasetFile = DatasetFileToProcess()
		datasetFile.dataset = datasetDBObject
		datasetFile.file_name = fileName

		return datasetFile

	def _createProcessNode(self, computerName, numThreads, hostname, port, status):
		processNode = ProcessNode()
		processNode.computer_name = computerName
		processNode.num_threads = numThreads
		processNode.hostname = hostname
		processNode.port = port
		processNode.status = status
		return processNode

	def _createStatus(self, status, description=None):
		return self._createNameDescriptionEntity(Status, status, description, nameAttribute='status')

	def _createJobStatus(self, statusName, processNodeId=None, startTime=None, finishTime=None, logPath=None):
		dbStatus = self.getStatus(statusName)
		jobStatus = JobStatus()

		if processNodeId:
			dbProcessNode = self.getProcessNodeById(processNodeId)
			jobStatus.process_node = dbProcessNode

		jobStatus.status = dbStatus
		jobStatus.start_proc_time = startTime
		jobStatus.finish_proc_time = finishTime
		jobStatus.log_path = logPath

		return jobStatus

	def _createJobEmail(self, email, attachment=None):
		jobEmail = JobEmail()
		jobEmail.email = email
		jobEmail.attachment = attachment

		return jobEmail

	def _createJob(self, isConcurrent, priority, softwareName, datasetPath, statusName, createdByUsername, dbEmails=None, emails=None, datasetFileNames=None):
		job = Job()

		job.is_concurrent = isConcurrent
		job.priority = priority

		software = self.softwareApi.getSoftwareByName(softwareName)
		job.experiment_software = software

		processAll = datasetPath is None
		dataset = self._createJobDataset(datasetPath, processAll)

		datasetFiles = []
		if not processAll:
			for datasetFileName in datasetFileNames:
				datasetFiles.append(self._createDatasetFileToProcess(dataset, datasetFileName))
		dataset.datasetFiles = datasetFiles

		job.dataset = dataset

		status = self.getStatus(statusName)
		job.job_status = status

		user = self.userApi.getUserByUsername(createdByUsername)
		job.submitted_by_user = user

		if dbEmails is not None:
			job.jobEmails = dbEmails
		elif emails is not None:
			dbEmails = []
			for email in emails:
				dbEmails.append(self._createJobEmail(email))
				job.jobEmails = dbEmails

		return job

	def getProcessNodes(self):
		return self._findAllDbObjects(ProcessNode)

	def getProcessNodeById(self, processNodeId):
		return self._findDbObjectByAttribute(ProcessNode, processNodeId, 'id')

	def addProcessNode(self, computerName, numThreads, hostname, port, status):
		processNode = self._createProcessNode(computerName, numThreads, hostname, port, status)

		self.session.add(processNode)
		self.session.commit()

		return processNode

	def getProcessNodeByComputerName(self, computerName):
		return self._findDbObjectByAttribute(ProcessNode, "computer_name", computerName)

	def updateProcessNodeStatus(self, computerName, status, heartbeat, processCpuPercent, processMemPercent,
	                            systemCpuPercent, systemMemPercent, systemSwapPercent):
		dbProcessNode = self.getProcessNodeByComputerName(computerName)

		dbProcessNode.heartbeat = heartbeat
		dbProcessNode.status = status
		dbProcessNode.process_cpu_percent = processCpuPercent
		dbProcessNode.process_mem_percent = processMemPercent
		dbProcessNode.system_cpu_percent = systemCpuPercent
		dbProcessNode.system_mem_percent = systemMemPercent
		dbProcessNode.system_swap_percent = systemSwapPercent

		self.session.add(dbProcessNode)
		self.session.commit()

		return dbProcessNode

	def getStatus(self, statusName):
		return self._findDbObjectByAttribute(Status, "status", statusName)


