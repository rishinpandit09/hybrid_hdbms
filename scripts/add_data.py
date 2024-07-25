from app import db, create_app
from app.models.Doctor import Doctor
from app.models.employee_model import Employee
from app.models.insurance_claim_model import InsuranceClaim
from app.models.inventory_model import InventoryItem
from app.models.invoice_model import Invoice
from app.models.patient_model import Patient

app = create_app()

with app.app_context():
    # Clear existing data
    db.drop_all()
    db.create_all()

    # Add doctors
    doctor1 = Doctor(name="Dr. Alice Smith", specialty="Cardiology")
    doctor2 = Doctor(name="Dr. Bob Johnson", specialty="Neurology")

    db.session.add(doctor1)
    db.session.add(doctor2)
    db.session.commit()

    # Add patients
    patient1 = Patient(name="John Doe", age=45, diagnosis="Heart Disease", treatment="Medication", doctor_id=doctor1.id)
    patient2 = Patient(name="Jane Roe", age=50, diagnosis="Brain Tumor", treatment="Surgery", doctor_id=doctor2.id)

    db.session.add(patient1)
    db.session.add(patient2)
    db.session.commit()

    # Add employees
    employee1 = Employee(name="Alice Johnson", role="Nurse", department="Cardiology")
    employee2 = Employee(name="Bob Smith", role="Technician", department="Neurology")

    db.session.add(employee1)
    db.session.add(employee2)
    db.session.commit()

    # Add insurance claims
    claim1 = InsuranceClaim(patient_id=patient1.id, amount=5000.0, status="Approved")
    claim2 = InsuranceClaim(patient_id=patient2.id, amount=10000.0, status="Pending")

    db.session.add(claim1)
    db.session.add(claim2)
    db.session.commit()

    # Add inventory items
    item1 = InventoryItem(name="Stethoscope", quantity=10, price=50.0)
    item2 = InventoryItem(name="MRI Machine", quantity=2, price=100000.0)

    db.session.add(item1)
    db.session.add(item2)
    db.session.commit()

    # Add invoices
    invoice1 = Invoice(amount=200.0, description="Consultation Fee", patient_id=patient1.id)
    invoice2 = Invoice(amount=500.0, description="MRI Scan", patient_id=patient2.id)

    db.session.add(invoice1)
    db.session.add(invoice2)
    db.session.commit()

    print("Data added successfully!")