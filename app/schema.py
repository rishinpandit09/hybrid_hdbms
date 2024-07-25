import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from app import db
from app.models.Doctor import Doctor
from app.models.employee_model import Employee
from app.models.insurance_claim_model import InsuranceClaim
from app.models.inventory_model import InventoryItem
from app.models.invoice_model import Invoice
from app.models.patient_model import Patient


class PatientObject(SQLAlchemyObjectType):
    class Meta:
        model = Patient
        interfaces = (graphene.relay.Node,)


class DoctorObject(SQLAlchemyObjectType):
    class Meta:
        model = Doctor
        interfaces = (graphene.relay.Node,)


class EmployeeObject(SQLAlchemyObjectType):
    class Meta:
        model = Employee
        interfaces = (graphene.relay.Node,)


class InsuranceClaimObject(SQLAlchemyObjectType):
    class Meta:
        model = InsuranceClaim
        interfaces = (graphene.relay.Node,)


class InventoryItemObject(SQLAlchemyObjectType):
    class Meta:
        model = InventoryItem
        interfaces = (graphene.relay.Node,)


class InvoiceObject(SQLAlchemyObjectType):
    class Meta:
        model = Invoice
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_patients = SQLAlchemyConnectionField(PatientObject)
    all_doctors = SQLAlchemyConnectionField(DoctorObject)
    all_employees = SQLAlchemyConnectionField(EmployeeObject)
    all_insurance_claims = SQLAlchemyConnectionField(InsuranceClaimObject)
    all_inventory_items = SQLAlchemyConnectionField(InventoryItemObject)
    all_invoices = SQLAlchemyConnectionField(InvoiceObject)


class CreatePatient(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        age = graphene.Int(required=True)
        diagnosis = graphene.String()
        treatment = graphene.String()
        doctor_id = graphene.Int()

    patient = graphene.Field(lambda: PatientObject)

    def mutate(self, info, name, age, diagnosis=None, treatment=None, doctor_id=None):
        patient = Patient(name=name, age=age, diagnosis=diagnosis, treatment=treatment, doctor_id=doctor_id)
        db.session.add(patient)
        db.session.commit()
        return CreatePatient(patient=patient)


class CreateDoctor(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        specialty = graphene.String(required=True)

    doctor = graphene.Field(lambda: DoctorObject)

    def mutate(self, info, name, specialty):
        doctor = Doctor(name=name, specialty=specialty)
        db.session.add(doctor)
        db.session.commit()
        return CreateDoctor(doctor=doctor)


class CreateEmployee(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        role = graphene.String(required=True)
        department = graphene.String()

    employee = graphene.Field(lambda: EmployeeObject)

    def mutate(self, info, name, role, department=None):
        employee = Employee(name=name, role=role, department=department)
        db.session.add(employee)
        db.session.commit()
        return CreateEmployee(employee=employee)


class CreateInsuranceClaim(graphene.Mutation):
    class Arguments:
        patient_id = graphene.Int(required=True)
        amount = graphene.Float(required=True)
        status = graphene.String(required=True)

    insurance_claim = graphene.Field(lambda: InsuranceClaimObject)

    def mutate(self, info, patient_id, amount, status):
        insurance_claim = InsuranceClaim(patient_id=patient_id, amount=amount, status=status)
        db.session.add(insurance_claim)
        db.session.commit()
        return CreateInsuranceClaim(insurance_claim=insurance_claim)


class CreateInventoryItem(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        quantity = graphene.Int(required=True)
        price = graphene.Float(required=True)

    inventory_item = graphene.Field(lambda: InventoryItemObject)

    def mutate(self, info, name, quantity, price):
        inventory_item = InventoryItem(name=name, quantity=quantity, price=price)
        db.session.add(inventory_item)
        db.session.commit()
        return CreateInventoryItem(inventory_item=inventory_item)


class CreateInvoice(graphene.Mutation):
    class Arguments:
        amount = graphene.Float(required=True)
        description = graphene.String()
        patient_id = graphene.Int(required=True)

    invoice = graphene.Field(lambda: InvoiceObject)

    def mutate(self, info, amount, description=None, patient_id=None):
        invoice = Invoice(amount=amount, description=description, patient_id=patient_id)
        db.session.add(invoice)
        db.session.commit()
        return CreateInvoice(invoice=invoice)


class Mutation(graphene.ObjectType):
    create_patient = CreatePatient.Field()
    create_doctor = CreateDoctor.Field()
    create_employee = CreateEmployee.Field()
    create_insurance_claim = CreateInsuranceClaim.Field()
    create_inventory_item = CreateInventoryItem.Field()
    create_invoice = CreateInvoice.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
