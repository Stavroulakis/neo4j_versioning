
class Deletion():
    def __init__(self):
        pass

    def delete_main_node(self, tx, node_name, node_type):
        """This function is responsible to delete the main node as well as all\
            its versions.

        Args:
            tx {class neo4j.work.transaction.Transaction}: The transaction \
                management with neo4j.
            node_name (String): The name of the node.
            node_type (String): The type (or label) of the node.
        """
        transaction = tx.run(
            "MATCH(node_1:" + node_type + "{Name:$node_1_name_state})<-[r1]-\
                (node_2:" + node_type + "{Name:$node_1_name})\
             DETACH DELETE node_1, node_2", node_1_name=node_name,
                                        node_1_name_state=node_name+"_State"
        )

    def delete_versions(self, tx, node_name, node_type, relation):
        """This function deletes all old versions of a specific node.

        Args:
            tx {class neo4j.work.transaction.Transaction}: The transaction \
                management with neo4j.
            node_name (String): The name of the node.
            node_type (String): The type (or label) of the node.
            relation (String): The name of relation which you want all the \
                versions. Default is 'Has_State'.
        """
        transaction = tx.run(
            "MATCH(node_1:" + node_type + "{Name:$node_1_name_state})<-[r1:\
                "+relation+"]-(node_2:" + node_type + "{Name:$node_1_name})\
                WHERE r1.To IS NOT null\
                    DETACH DELETE node_1",
            node_1_name=node_name, node_1_name_state=node_name+"_State"
        )
