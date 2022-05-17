# from src.neo4j_versioning import Neo4j_versioning
from neo4jVersioning.src.neo4jVersioning import neo4jVersioning

host = 'neo4j://localhost:7687'
user = 'neo4j'
passwd = '1234'

nv = neo4jVersioning(host,user,passwd)
node = {'Name':'Customer1','Type':'type1','Properties':{'LastName':'Doc','Email':'Dco@.com'}}

state = nv.process_node(node,'graph.db')
# print(state)

# properties= nv.node_properties(node,'graph.db')
# print(properties)
# versions = nv.node_versions(node, 'graph.db')
# print(versions)
# properties= nv.node_properties(node,'graph.db')
# print(properties)
# print(versions['Version_1'])
# properties2 = nv.node_properties(node,'graph.db',versions['Version_1'])
# print(properties2)
# nv.delete_node_versions(node,'graph.db',"Has_Docs")
# all_nodes = nv.get_all_nodes()
# print(all_nodes)