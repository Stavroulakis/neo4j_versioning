from neo4j import GraphDatabase
from .helper_functions.write import Write
from .helper_functions.check import Check
from .helper_functions.deletion import Deletion
from .helper_functions.fetch import Fetch
from .logger import get_logger


class neo4jVersioning():
    def __init__(self, host, user, passwd):
        self.driver = GraphDatabase.driver(host, auth=(user, passwd))
        self.writer = Write()
        self.checker = Check()
        self.delete = Deletion()
        self.fetcher = Fetch()
        self.logger = get_logger(__name__)

    def process_node(self, node, database='graph.db', relation="Has_State"):
        with self.driver.session(database=database) as session:
            node_name = node['Name']
            node_type = node['Type']
            node_properties = node['Properties']
            # Check if this node with this state exist
            node_with_state = session.write_transaction(
                self.checker.check_node_state,  node_name, node_type,
                node_properties, relation
            )
            # if not: check if this node exist with different state
            if not node_with_state:
                main_node = session.write_transaction(
                    self.checker.check_main_node, node_type, node_name
                )
                # if main node exist: update with new state, else create a new
                # node-state relationship
                if main_node:
                    session.write_transaction(
                        self.writer.update_node_state, node_type, node_name,
                        node_properties, relation
                    )
                    self.logger.info(f"Node {node_name} \
                        got an updated version")
                else:
                    session.write_transaction(
                        self.writer.write_node_with_state, node_type,
                        node_name, node_properties, relation
                    )
                    self.logger.info(f"New node ({node_name}) has been added\
                        to the database")
            else:
                self.logger.info(f"Node {node_name} is up to date")

    def node_properties(self, node, database='graph.db', version='null',
                        relation='Has_State'):
        with self.driver.session(database=database) as session:
            node_name = node['Name']
            node_type = node['Type']
            node_properties = session.write_transaction(
                self.fetcher.get_node_properties, node_name,  node_type,
                version, relation
            )
        return node_properties

    def node_versions(self, node, database='graph.db', relation='Has_State'):
        with self.driver.session(database=database) as session:
            node_name = node['Name']
            node_type = node['Type']
            node_versions = session.write_transaction(
                self.fetcher.get_node_versions, node_name, node_type, relation
            )
        return node_versions

    def create_relationship(self, node_1, node_2, relation,
                            database='graph.db'):
        with self.driver.session(database=database) as session:
            node_1_name = node_1['Name']
            node_1_type = node_1['Type']
            node_2_name = node_2['Name']
            node_2_type = node_2['Type']
            session.write_transaction(
                self.writer.create_new_relation, node_1_name, node_1_type,
                node_2_name, node_2_type, relation
            )

    def delete_node(self, node, database='graph.db'):
        with self.driver.session(database=database) as session:
            node_name = node['Name']
            node_type = node['Type']
            deleted_node = session.write_transaction(
                self.delete.delete_main_node, node_name, node_type
            )
        self.logger.info(f"Node {node_name} and all its versions \
                        have been deleted ")
        return deleted_node

    def delete_node_versions(self, node, database='graph.db',
                             relation='Has_State'):
        with self.driver.session(database=database) as session:
            node_name = node['Name']
            node_type = node['Type']
            deleted_node_versions = session.write_transaction(
                self.delete.delete_versions, node_name, node_type, relation
            )
        self.logger.info(f" All previous versions of node {node_name} \
            have been deleted ")
        return deleted_node_versions

    def get_main_nodes(self, database='graph.db'):
        with self.driver.session(database=database) as session:
            all_nodes = session.write_transaction(
                self.fetcher.get_all_main_nodes
            )
        return all_nodes

    def node_type(self, node_name, database='graph.db'):
        with self.driver.session(database=database) as session:
            node_type = session.write_transaction(
                self.fetcher.get_node_type, node_name
            )
        return node_type
