from ..src.neo4j_versioning import Neo4j_versioning

host = 'http://localhost:7474'
user = 'neo4j'
passwd = '1234'

nv = Neo4j_versioning(host,user,passwd)

node = {'name':'testname','type':'type1','properties':{'prop1':'temp1','prop2':'temp2'}}

state = nv.process_node(node,'default')
print(state)