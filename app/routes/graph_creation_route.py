from flask_restful import Resource
from py2neo import Graph, Node, Relationship

from app.models.doctor_model import Doctor
from app.models.employee_model import Employee
from app.models.insurance_claim_model import InsuranceClaim
from app.models.inventory_model import InventoryItem
from app.models.invoice_model import Invoice
from app.models.patient_model import Patient

class CreateGraphInMemgraph(Resource):
    def get(self):
        graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))

        # Clear existing graph
        graph.run("MATCH (n) DETACH DELETE n")

        # Collect nodes and relationships
        nodes = {}
        relationships = []

        # Insert nodes and relationships
        self.insert_patients(graph, nodes, relationships)
        self.insert_doctors(graph, nodes)
        self.insert_employees(graph, nodes)
        self.insert_insurance_claims(graph, nodes, relationships)
        self.insert_inventory_items(graph, nodes)
        self.insert_invoices(graph, nodes, relationships)

        return {
            "message": "Graph created in Memgraph",
            "nodes": list(nodes.values()),
            "relationships": relationships
        }

    def insert_patients(self, graph, nodes, relationships):
        patients = Patient.query.all()
        for patient in patients:
            patient_node = Node("Patient", id=patient.id, name=patient.name, age=patient.age, diagnosis=patient.diagnosis, treatment=patient.treatment)
            graph.create(patient_node)
            nodes[patient.id] = {
                "id": patient_node.identity,
                "labels": ["Patient"],
                "properties": {
                    "id": patient.id,
                    "name": patient.name,
                    "age": patient.age,
                    "diagnosis": patient.diagnosis,
                    "treatment": patient.treatment
                },
                "type": "node"
            }
            if patient.doctor_id:
                doctor = Doctor.query.get(patient.doctor_id)
                doctor_node = Node("Doctor", id=doctor.id, name=doctor.name, specialty=doctor.specialty)
                graph.merge(doctor_node, "Doctor", "id")
                relationship = Relationship(patient_node, "TREATED_BY", doctor_node)
                graph.create(relationship)
                nodes[doctor.id] = {
                    "id": doctor_node.identity,
                    "labels": ["Doctor"],
                    "properties": {
                        "id": doctor.id,
                        "name": doctor.name,
                        "specialty": doctor.specialty
                    },
                    "type": "node"
                }
                relationships.append({
                    "id": relationship.identity,
                    "start": patient_node.identity,
                    "end": doctor_node.identity,
                    "label": "TREATED_BY",
                    "properties": {},
                    "type": "relationship"
                })

    def insert_doctors(self, graph, nodes):
        doctors = Doctor.query.all()
        for doctor in doctors:
            doctor_node = Node("Doctor", id=doctor.id, name=doctor.name, specialty=doctor.specialty)
            graph.create(doctor_node)
            nodes[doctor.id] = {
                "id": doctor_node.identity,
                "labels": ["Doctor"],
                "properties": {
                    "id": doctor.id,
                    "name": doctor.name,
                    "specialty": doctor.specialty
                },
                "type": "node"
            }

    def insert_employees(self, graph, nodes):
        employees = Employee.query.all()
        for employee in employees:
            employee_node = Node("Employee", id=employee.id, name=employee.name, role=employee.role, department=employee.department)
            graph.create(employee_node)
            nodes[employee.id] = {
                "id": employee_node.identity,
                "labels": ["Employee"],
                "properties": {
                    "id": employee.id,
                    "name": employee.name,
                    "role": employee.role,
                    "department": employee.department
                },
                "type": "node"
            }

    def insert_insurance_claims(self, graph, nodes, relationships):
        insurance_claims = InsuranceClaim.query.all()
        for claim in insurance_claims:
            claim_node = Node("InsuranceClaim", id=claim.id, patient_id=claim.patient_id, amount=claim.amount, status=claim.status)
            graph.create(claim_node)
            nodes[claim.id] = {
                "id": claim_node.identity,
                "labels": ["InsuranceClaim"],
                "properties": {
                    "id": claim.id,
                    "patient_id": claim.patient_id,
                    "amount": claim.amount,
                    "status": claim.status
                },
                "type": "node"
            }
            patient = Patient.query.get(claim.patient_id)
            if patient:
                patient_node = Node("Patient", id=patient.id, name=patient.name, age=patient.age, diagnosis=patient.diagnosis, treatment=patient.treatment)
                graph.merge(patient_node, "Patient", "id")
                relationship = Relationship(claim_node, "BELONGS_TO", patient_node)
                graph.create(relationship)
                nodes[patient.id] = {
                    "id": patient_node.identity,
                    "labels": ["Patient"],
                    "properties": {
                        "id": patient.id,
                        "name": patient.name,
                        "age": patient.age,
                        "diagnosis": patient.diagnosis,
                        "treatment": patient.treatment
                    },
                    "type": "node"
                }
                relationships.append({
                    "id": relationship.identity,
                    "start": claim_node.identity,
                    "end": patient_node.identity,
                    "label": "BELONGS_TO",
                    "properties": {},
                    "type": "relationship"
                })

    def insert_inventory_items(self, graph, nodes):
        inventory_items = InventoryItem.query.all()
        for item in inventory_items:
            item_node = Node("InventoryItem", id=item.id, name=item.name, quantity=item.quantity, price=item.price)
            graph.create(item_node)
            nodes[item.id] = {
                "id": item_node.identity,
                "labels": ["InventoryItem"],
                "properties": {
                    "id": item.id,
                    "name": item.name,
                    "quantity": item.quantity,
                    "price": item.price
                },
                "type": "node"
            }

    def insert_invoices(self, graph, nodes, relationships):
        invoices = Invoice.query.all()
        for invoice in invoices:
            invoice_node = Node("Invoice", id=invoice.id, amount=invoice.amount, description=invoice.description)
            graph.create(invoice_node)
            nodes[invoice.id] = {
                "id": invoice_node.identity,
                "labels": ["Invoice"],
                "properties": {
                    "id": invoice.id,
                    "amount": invoice.amount,
                    "description": invoice.description
                },
                "type": "node"
            }
            patient = Patient.query.get(invoice.patient_id)
            if patient:
                patient_node = Node("Patient", id=patient.id, name=patient.name, age=patient.age, diagnosis=patient.diagnosis, treatment=patient.treatment)
                graph.merge(patient_node, "Patient", "id")
                relationship = Relationship(invoice_node, "ISSUED_TO", patient_node)
                graph.create(relationship)
                nodes[patient.id] = {
                    "id": patient_node.identity,
                    "labels": ["Patient"],
                    "properties": {
                        "id": patient.id,
                        "name": patient.name,
                        "age": patient.age,
                        "diagnosis": patient.diagnosis,
                        "treatment": patient.treatment
                    },
                    "type": "node"
                }
                relationships.append({
                    "id": relationship.identity,
                    "start": invoice_node.identity,
                    "end": patient_node.identity,
                    "label": "ISSUED_TO",
                    "properties": {},
                    "type": "relationship"
                })
