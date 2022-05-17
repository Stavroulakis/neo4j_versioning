from src.neo4j_versioning import Neo4j_versioning
host = 'neo4j://localhost:7687'
user = 'neo4j'
passwd = '1234'

neov = Neo4j_versioning(host,user,passwd)

#### Get all nodes from db #####
all_nodes = neov.get_main_nodes()

## Get the type of one node
nodeName = all_nodes[0]
node_type = neov.node_type(nodeName)
print(node_type)

# create a node Dictionary
node = {'name':nodeName,'type':node_type}

## Get all node's versions
node_version = neov.node_versions(node)
print(node_version)

## Get node's properties of specific version
node_props_v1 = neov.node_properties(node,version=node_version['Version_1'])
print(node_props_v1)
node_props = neov.node_properties(node)
print(node_props)