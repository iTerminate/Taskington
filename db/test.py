from api.JobApi import JobApi
from api.SoftwareApi import SoftwareApi
from db.api.UserApi import UserApi

userApi = UserApi()
softwareApi = SoftwareApi()
jobApi = JobApi()

userApi.addRole("testRole", "some description")

userApi.addUser('djarosz','4#ES$@#S', "Another Test Role")
userApi.addUser('aglowacki','4#ES$@#S', "Another Test Role")
userApi.addUser('someUser', roleName="testRole")
userApi.addUser("noRole")
userApi.addBeamline("2", 'stuff')
userApi.addBeamline("4")
userApi.addBeamline("6")
userApi.addBeamline("35")
userApi.addBeamline("9")

user = userApi.getUserByUsername('djarosz')
user2 = userApi.getUserByUsername('noRole')

userApi.assignUserRoles('djarosz', ['user', 'standard', 'testRole'])
userApi.assignUserBeamline('djarosz', ["2", "4", "some other beamline", "yet another one !!!"])

mapsPySoftware = "Maps-Py"
ptychoLibSoftware = "Ptycholib"
argType="Integer"
softwareApi.addSoftware(mapsPySoftware)
softwareApi.addArgumentType(argType)
softwareApi.addSoftwareArg(mapsPySoftware, argType, "Some-min")
softwareApi.addSoftwareArg(mapsPySoftware, argType, "Some-max")

softwareApi.addSoftware(ptychoLibSoftware)
softwareApi.addSoftwareArg(ptychoLibSoftware, argType, "Some-mi2")
softwareApi.addSoftwareArg(ptychoLibSoftware, argType, "Some-num")
softwareApi.addSoftwareArg(ptychoLibSoftware, argType, "Some-min")
softwareApi.addSoftwareArg(ptychoLibSoftware, argType, "Some-max")



def testPrintList(title, list, attribute = 'name'):
	print '**************' + title + '**************'
	for idx, item in enumerate(list):
		print str(idx) + ' - ' + getattr(item, attribute)
	print '*****************************************'

users = userApi.getUsers()
beamlines = userApi.getBeamlines()
roles = userApi.getRoles()
testPrintList("Users", users, attribute='username')
testPrintList("Roles", roles)
testPrintList("Beamlines", beamlines)

dbSoftwareList = softwareApi.getSoftware()

for dbSoftware in dbSoftwareList:
	testPrintList(dbSoftware.name + " keys", dbSoftware.softwareArguments, attribute="key")





