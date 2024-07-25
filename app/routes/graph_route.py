from flask_restful import Resource
from py2neo import Graph
from flask import jsonify
import json

class GraphRepresentationResource(Resource):
    def get(self):
        graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
        query = """
        MATCH (n)-[r]->(m)
        RETURN n, r, m
        """
        result = graph.run(query)
        nodes = []
        relationships = []

        for record in result:
            nodes.append({
                "id": record["n"].identity,
                "label": list(record["n"].labels)[0],
                "properties": dict(record["n"])
            })
            nodes.append({
                "id": record["m"].identity,
                "label": list(record["m"].labels)[0],
                "properties": dict(record["m"])
            })
            relationships.append({
                "id": record["r"].identity,
                "start_node": record["r"].start_node.identity,
                "end_node": record["r"].end_node.identity,
                "type": record["r"].type,
                "properties": dict(record["r"])
            })

        # Remove duplicates
        unique_nodes = list({json.dumps(node, sort_keys=True): node for node in nodes}.values())

        return jsonify({
            "nodes": unique_nodes,
            "relationships": relationships
        })
