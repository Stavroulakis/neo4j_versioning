from .handlers import Handlers


class Check():
    def __init__(self):
        self.handler = Handlers()

    def check_node_state(self, tx, node_name, node_type, properties, relation):
        """This functions checks if the specific node with Name, Type \
            and these properties exist in the database

        Args:
             tx {class neo4j.work.transaction.Transaction}: The transaction \
                management with neo4j.
            node_name (String): The name of the node.
            node_type (String): The type (or label) of the node.
            properties (Dict): The propertiesd of a node
            relation (String): The name of relation which you want all the \
                versions. Default is 'Has_State'.

        Returns:
            Int: 0 if it is not exist,  1 if it exist
        """
        string_properties = self.handler.get_string_properties(properties,
                                                               node_name)
        transaction = tx.run(
            "MATCH (node_1:" + node_type + "{Name:$node_1_name})\
            -[node_relation:"+relation+"]-> (node_2:" + node_type + "\
                {" + string_properties + "}" + ")\
                    WHERE node_relation.To IS NULL\
                        RETURN count(node_1) as exist",
            node_1_name=node_name
        )
        a_key = "exist"
        values_of_key = [a_dict[a_key] for a_dict in transaction.data()]
        return int(values_of_key[0])

    def check_main_node(self, tx, node_type, node_name):
        """This function check if main node with the specific type and name\
            exist

        Args:
             tx {class neo4j.work.transaction.Transaction}: The transaction \
                management with neo4j.
            node_name (String): The name of the node.
            node_type (String): The type (or label) of the node.

        Returns:
            Int: 0 if it is not exist,  1 if it exist
        """
        transaction = tx.run(
            "MATCH (node_1:" + node_type + "{Name:$node_1_name})\
             RETURN count(node_1) as exist",
            node_1_name=node_name
        )
        a_key = "exist"
        values_of_key = [a_dict[a_key] for a_dict in transaction.data()]
        return int(values_of_key[0])
