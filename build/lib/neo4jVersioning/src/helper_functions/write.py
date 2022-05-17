from datetime import datetime
from .handlers import Handlers


class Write():
    def __init__(self):
        self.handler = Handlers()

    def write_node_with_state(self, tx, node_type, node_name,
                              properties, relation):
        """This function is responsible to create a new node and the state \
            node with its properties

        Args:
            tx {class neo4j.work.transaction.Transaction}: The transaction \
                management with neo4j.
            node_name (String): The name of the node.
            node_type (String): The type (or label) of the node.
            properties (Dict): The propertiesd of a node
            relation (String): The name of relation which you want all the \
                versions. Default is 'Has_State'.
        """
        string_properties = self.handler.get_string_properties(properties,
                                                               node_name)
        transaction = tx.run(
            "MERGE (node_1:" + node_type + "{Name:$node_1_name})\
            -[node_relation:"+relation+" {From:$fromDate}]-> \
                (node_2:" + node_type + " {" + string_properties+"}" + ")\
                    RETURN node_1, node_2",
            node_1_name=node_name, props=properties,
            node_2_name=f'{node_name}_State', fromDate=str(datetime.now())
        )

    def update_node_state(self, tx, node_type, node_name,
                          properties, relation):
        """This function updates the node with a new version

        Args:
            tx {class neo4j.work.transaction.Transaction}: The transaction \
                management with neo4j.
            node_name (String): The name of the node.
            node_type (String): The type (or label) of the node.
            properties (Dict): The propertiesd of a node
            relation (String): The name of relation which you want all the \
                versions. Default is 'Has_State'.

        """
        set_old_version = tx.run(
            "MATCH (node_1:" + node_type+"{Name:$node_1_name})\
            -[node_relation:"+relation+"]-> (node_2:" + node_type + "\
                {Name:$node_1_name_state})\
             WHERE node_relation.To IS NULL \
             SET node_relation +={To:$fromDate}",
            node_1_name=node_name, node_1_name_state=f'{node_name}_State',
            fromDate=str(datetime.now())
        )
        string_properties = self.handler.get_string_properties(properties,
                                                               node_name)
        set_new_version = tx.run(
            "MATCH (node_1:" + node_type + "{Name:$node_1_name})\
            CREATE (node_2:" + node_type + " {" + string_properties+"}"+")\
            CREATE (node_1)-[node_relation:"+relation+" {From:$fromDate}]->\
                                                                    (node_2)\
            RETURN node_2", node_1_name=node_name, fromDate=str(datetime.now())
        )

    def create_new_relation(self, tx, node_1_name, node_1_type, node_2_name,
                            node_2_type, relation):
        """This function is responsible for the creation of relation between \
            two main nodes

        Args:
            tx {class neo4j.work.transaction.Transaction}: The transaction \
                management with neo4j.
            node_1_name (String):The name of the first node
            node_1_type (String):The type of the first node
            node_2_name (String):The name of the second node
            node_2_type (String):The type of the second node
            relation (String): The relation that will connect the two nodes

        Returns:
            [type]: [description]
        """
        transaction = tx.run(
            "MATCH (node_1:"+node_1_type+" {Name:$node_1_name})\
             MATCH (node_2:"+node_2_type+" {Name:$node_2_name})\
             MERGE (node_1)-[r:"+relation+" {From:$fromDate}]->(node_2)\
             RETURN node_1, node_2, r",
            node_1_name=node_1_name, node_2_name=node_2_name,
            fromDate=str(datetime.now())
        )
        return transaction.data()
