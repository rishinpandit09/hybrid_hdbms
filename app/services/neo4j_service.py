from app import neo4j_driver


def add_patient_to_neo4j(name, age):
    with neo4j_driver.session() as session:
        session.run("CREATE (p:Patient {name: $name, age: $age})", name=name, age=age)


def get_patient_relationships():
    with neo4j_driver.session() as session:
        result = session.run("MATCH (p:Patient)-[r]->(n) RETURN p, r, n")
        relationships = []
        for record in result:
            relationships.append({
                "patient": record["p"]["name"],
                "relationship": record["r"].type,
                "related_entity": record["n"]["name"]
            })
    return relationships
