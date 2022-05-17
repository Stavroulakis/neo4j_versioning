
class Fetch():
    def __init__(self):
        pass

    def get_node_properties(self, tx, node_name, node_type, version, relation):
        """This function is fetching all the properties of a specific\
            node's version

        Args:
            tx {class neo4j.work.transaction.Transaction}: The transaction \
                management with neo4j.
            node_name (String): The name of the node.
            node_type (String): The type (or label) of the node.
            version (String): The version on which the properties are\
                 requested. If null, it will fetch the current updated version.
            relation (String): The name of relation which is conencted with\
                the properties. Default is 'Has_State'.

        Returns:
            Dict: A dictonary of all properties
        """
        if version == 'null':
            transaction = tx.run(
                "MATCH(node_1:" + node_type + ")<-[r1:" + relation + "]-\
                    (node_2:" + node_type + ")\
                        WHERE r1.To is " + version + " AND node_1.Name ='" +
                                            node_name + "_" +
                                            relation.split("_")[1]+"'\
                            RETURN properties(node_1)"
            )
        else:
            transaction = tx.run(
                "MATCH(node_1:" + node_type + ")<-[r1:" + relation + "]-\
                    (node_2:" + node_type + ")\
                        WHERE r1.To ='" + version + "' AND node_1.Name ='" +
                                            node_name + "_" +
                                            relation.split("_")[1] + "'\
                            RETURN properties(node_1)"
            )
        values_of_key = [a_dict['properties(node_1)'] for a_dict
                         in transaction.data()]
        return values_of_key[0]

    def get_node_versions(self, tx, node_name, node_type, relation):
        """ This function is fetching all the versions of a node with \
            respect to relation name (Default Has_State)

        Args:
            tx {class neo4j.work.transaction.Transaction}: The transaction\
                management with neo4j
            node_name (String): The name of the node
            node_type (String): The type (or label) of the node
            relation (String): The name of relation which you want all \
                the versions. Default is 'Has_State'

        Returns:
            Dict: A dictionary of all versions of a node. \
                Format: {Current_version, Version_1,Version_2...}
        """
        transaction = tx.run(
            "MATCH (node_1:" + node_type + "{Name:$node_1_name})\
                -[node_relation:"+relation+"]->(node_2:"+node_type+")\
                    RETURN properties(node_relation) ORDER BY \
                        node_relation.To DESC", node_1_name=node_name
        )
        featched_data = transaction.data()
        num_of_versions = len(featched_data)
        counter = 0
        versions = {}
        for entry in featched_data:
            if counter == 0:
                versions['Current_version'] = entry[
                    'properties(node_relation)']['From']
            else:
                versions['Version_'+str(num_of_versions-counter)] = entry[
                    'properties(node_relation)']['To']
            counter += 1
        return versions

    def get_all_main_nodes(self, tx):
        """This function is fetching all 'Main' nodes

        Args:
            tx {class neo4j.work.transaction.Transaction}: The transaction \
                management with neo4j

        Returns:
            List: List with the names of all 'Main' Nodes in ddatabase
        """
        transaction = tx.run(
            "MATCH (node_1)-[r1]->(node_2)\
                WHERE r1.To is null\
                    RETURN node_1"
        )
        collected_data = transaction.values()
        nodes = []
        for node in collected_data:
            nodes.append(node[0].get("Name"))
        return list(set(nodes))

    def get_node_type(self, tx, node_name):
        """This function is fetching the type (label) of a node

        Args:
            tx {class neo4j.work.transaction.Transaction}: The transaction \
                management with neo4j
            node_name (String): The name of the node

        Returns:
            String: The type (label) of the node
        """
        transaction = tx.run(
            "MATCH (node_1) WHERE node_1.Name ='"+node_name+"' \
                RETURN labels(node_1)"
        )
        values_of_key = [a_dict['labels(node_1)'] for a_dict
                         in transaction.data()]
        return values_of_key[0][0]
