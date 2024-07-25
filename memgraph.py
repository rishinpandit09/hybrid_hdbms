from py2neo import Graph, Node


def get_memgraph_connection():
    return Graph("bolt://localhost:7687", auth=("neo4j", "password"))


def insert_patient_to_memgraph(patient_id, name, age, diagnosis, treatment, doctor_id):
    graph = get_memgraph_connection()
    patient_node = Node("Patient", id=patient_id, name=name, age=age, diagnosis=diagnosis, treatment=treatment,
                        doctor_id=doctor_id)
    graph.create(patient_node)


def insert_doctor_to_memgraph(doctor_id, name, specialty):
    graph = get_memgraph_connection()
    doctor_node = Node("Doctor", id=doctor_id, name=name, specialty=specialty)
    graph.create(doctor_node)
