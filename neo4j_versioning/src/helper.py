
class Helper():
    def __init__(self):
        pass

    def check_node_state(self, tx, node_type, node_name, props):
        string_props = self.get_string_props(props, node_name)
        result = tx.run(
            "MATCH (node_1:" + node_type + "{Name:$node_1_name})\
            -[node_relation:Has_State]-> (node_2:" + node_type + "{" + string_props + "}" + ")\
             WHERE node_relation.To IS NULL\
             RETURN count(node_1) as exist",
            node_1_name=node_name
        )
        a_key = "exist"
        values_of_key = [a_dict[a_key] for a_dict in result.data()]
        self.logger.info("check node with state to exist")
        self.logger.info(values_of_key[0])
        return values_of_key[0]