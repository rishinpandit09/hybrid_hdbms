from flask_restful import Resource
from py2neo import Graph, Node, Relationship

from app.models.Doctor import Doctor
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

        # Insert nodes and relationships
        self.insert_patients(graph)
        self.insert_doctors(graph)
        self.insert_employees(graph)
        self.insert_insurance_claims(graph)
        self.insert_inventory_items(graph)
        self.insert_invoices(graph)

        return {"message": "Graph created in Memgraph"}

    def insert_patients(self, graph):
        patients = Patient.query.all()
        for patient in patients:
            patient_node = Node("Patient", id=patient.id, name=patient.name, age=patient.age, diagnosis=patient.diagnosis, treatment=patient.treatment)
            graph.create(patient_node)
            if patient.doctor_id:
                doctor = Doctor.query.get(patient.doctor_id)
                doctor_node = Node("Doctor", id=doctor.id, name=doctor.name, specialty=doctor.specialty)
                graph.merge(doctor_node, "Doctor", "id")
                relationship = Relationship(patient_node, "TREATED_BY", doctor_node)
                graph.create(relationship)

    def insert_doctors(self, graph):
        doctors = Doctor.query.all()
        for doctor in doctors:
            doctor_node = Node("Doctor", id=doctor.id, name=doctor.name, specialty=doctor.specialty)
            graph.create(doctor_node)

    def insert_employees(self, graph):
        employees = Employee.query.all()
        for employee in employees:
            employee_node = Node("Employee", id=employee.id, name=employee.name, role=employee.role, department=employee.department)
            graph.create(employee_node)

    def insert_insurance_claims(self, graph):
        insurance_claims = InsuranceClaim.query.all()
        for claim in insurance_claims:
            claim_node = Node("InsuranceClaim", id=claim.id, patient_id=claim.patient_id, amount=claim.amount, status=claim.status)
            graph.create(claim_node)
            patient = Patient.query.get(claim.patient_id)
            if patient:
                patient_node = Node("Patient", id=patient.id, name=patient.name, age=patient.age, diagnosis=patient.diagnosis, treatment=patient.treatment)
                graph.merge(patient_node, "Patient", "id")
                relationship = Relationship(claim_node, "BELONGS_TO", patient_node)
                graph.create(relationship)

    def insert_inventory_items(self, graph):
        inventory_items = InventoryItem.query.all()
        for item in inventory_items:
            item_node = Node("InventoryItem", id=item.id, name=item.name, quantity=item.quantity, price=item.price)
            graph.create(item_node)

    def insert_invoices(self, graph):
        invoices = Invoice.query.all()
        for invoice in invoices:
            invoice_node = Node("Invoice", id=invoice.id, amount=invoice.amount, description=invoice.description)
            graph.create(invoice_node)
            patient = Patient.query.get(invoice.patient_id)
            if patient:
                patient_node = Node("Patient", id=patient.id, name=patient.name, age=patient.age, diagnosis=patient.diagnosis, treatment=patient.treatment)
                graph.merge(patient_node, "Patient", "id")
                relationship = Relationship(invoice_node, "ISSUED_TO", patient_node)
                graph.create(relationship)
