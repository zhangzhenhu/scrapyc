import xmlrpclib

server = xmlrpclib.ServerProxy('http://localhost:5000/api')

print server.system.listMethods()
print server.list_jobs()
