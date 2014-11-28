import xmlrpclib

server = xmlrpclib.ServerProxy('http://localhost:5000/api')
import pdb
print server.system.listMethods()
pdb.set_trace()
#print server.list_jobs()
