from neo4j import GraphDatabase
from helper import Helper

class Neo4j_versioning():
    def __init__(self,host,user,passwd):
        self.driver = GraphDatabase.driver(host,auth=(user,passwd))

    def process_node(self,node,database_name):
        with self.driver.session(database=database_name) as session:
            node_name = node['name']
            node_type = node['type']
            node_properties = node['properties']
            # Check if this node with state exist
            node_with_state = session.write_transaction(
                Helper.check_node_state, node_name, node_type, node_properties
            )
        return node_with_state