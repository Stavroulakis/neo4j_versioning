
class Handlers():
    def __init__(self):
        pass

    def get_string_properties(self, properties, node_name):
        """This helper function is repsonsible to create node's properties \
            in specific format to be accepted by neo4j query mechanism

        Args:
            properties (Dict): The proeprties of the node
            node_name (String): The node name
        Returns:
            String: Properties in string format
        """
        properties['Name'] = node_name+"_State"
        stringDict = ""
        if isinstance(properties, list):
            for property in properties:
                if property == 'Name':
                    stringDict += property.strip('"') + \
                        ":" + "'"+node_name+"_State'" + ","
                else:
                    stringDict += property.strip('"') + \
                        ":" + "'"+property+"'" + ","
            return stringDict[:-1]
        else:
            for key, value in properties.items():
                stringDict += key.strip('"')+":" + "'"+value+"'" + ","
            return stringDict[:-1]
