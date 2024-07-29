from app import db, create_app
from app.models.doctor_model import Doctor
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
    doctors = [
        Doctor(name="Dr. Alice Smith", specialty="Cardiology"),
        Doctor(name="Dr. Bob Johnson", specialty="Neurology"),
        Doctor(name="Dr. Carol Lee", specialty="Orthopedics"),
        Doctor(name="Dr. David Kim", specialty="Dermatology"),
        Doctor(name="Dr. Eva Green", specialty="Pediatrics"),
        Doctor(name="Dr. Frank Brown", specialty="Oncology"),
        Doctor(name="Dr. Grace White", specialty="Gastroenterology"),
        Doctor(name="Dr. Henry Black", specialty="Urology"),
        Doctor(name="Dr. Irene Blue", specialty="Endocrinology"),
        Doctor(name="Dr. Jack Grey", specialty="Psychiatry")
    ]
    db.session.bulk_save_objects(doctors)
    db.session.commit()

    # Add patients
    patients = [
        Patient(name="John Doe", age=45, diagnosis="Heart Disease", treatment="Medication", doctor_id=doctors[0].id),
        Patient(name="Jane Roe", age=50, diagnosis="Brain Tumor", treatment="Surgery", doctor_id=doctors[1].id),
        Patient(name="Jake Paul", age=35, diagnosis="Fracture", treatment="Cast", doctor_id=doctors[2].id),
        Patient(name="Lily Evans", age=28, diagnosis="Eczema", treatment="Ointment", doctor_id=doctors[3].id),
        Patient(name="Harry Potter", age=10, diagnosis="Asthma", treatment="Inhaler", doctor_id=doctors[4].id),
        Patient(name="Sam Wilson", age=55, diagnosis="Lung Cancer", treatment="Chemotherapy", doctor_id=doctors[5].id),
        Patient(name="Mary Jane", age=60, diagnosis="Ulcer", treatment="Antacids", doctor_id=doctors[6].id),
        Patient(name="Peter Parker", age=40, diagnosis="Kidney Stones", treatment="Surgery", doctor_id=doctors[7].id),
        Patient(name="Tony Stark", age=50, diagnosis="Diabetes", treatment="Insulin", doctor_id=doctors[8].id),
        Patient(name="Bruce Wayne", age=35, diagnosis="Depression", treatment="Therapy", doctor_id=doctors[9].id)
    ]
    db.session.bulk_save_objects(patients)
    db.session.commit()

    # Add employees
    employees = [
        Employee(name="Alice Johnson", role="Nurse", department="Cardiology"),
        Employee(name="Bob Smith", role="Technician", department="Neurology"),
        Employee(name="Charlie Brown", role="Receptionist", department="Orthopedics"),
        Employee(name="David Williams", role="Pharmacist", department="Dermatology"),
        Employee(name="Eve Davis", role="Nurse", department="Pediatrics"),
        Employee(name="Frank Thomas", role="Technician", department="Oncology"),
        Employee(name="Grace Martin", role="Receptionist", department="Gastroenterology"),
        Employee(name="Henry Jackson", role="Pharmacist", department="Urology"),
        Employee(name="Irene Lee", role="Nurse", department="Endocrinology"),
        Employee(name="Jack Harris", role="Technician", department="Psychiatry")
    ]
    db.session.bulk_save_objects(employees)
    db.session.commit()

    # Add insurance claims
    insurance_claims = [
        InsuranceClaim(patient_id=patients[0].id, amount=5000.0, status="Approved"),
        InsuranceClaim(patient_id=patients[1].id, amount=10000.0, status="Pending"),
        InsuranceClaim(patient_id=patients[2].id, amount=3000.0, status="Denied"),
        InsuranceClaim(patient_id=patients[3].id, amount=4000.0, status="Approved"),
        InsuranceClaim(patient_id=patients[4].id, amount=2000.0, status="Pending"),
        InsuranceClaim(patient_id=patients[5].id, amount=15000.0, status="Approved"),
        InsuranceClaim(patient_id=patients[6].id, amount=8000.0, status="Denied"),
        InsuranceClaim(patient_id=patients[7].id, amount=6000.0, status="Approved"),
        InsuranceClaim(patient_id=patients[8].id, amount=7000.0, status="Pending"),
        InsuranceClaim(patient_id=patients[9].id, amount=5000.0, status="Approved")
    ]
    for claim in insurance_claims:
        db.session.add(claim)
    db.session.commit()

    # Add inventory items
    inventory_items = [
        InventoryItem(name="Stethoscope", quantity=10, price=50.0),
        InventoryItem(name="MRI Machine", quantity=2, price=100000.0),
        InventoryItem(name="X-Ray Machine", quantity=3, price=75000.0),
        InventoryItem(name="Ultrasound Machine", quantity=4, price=50000.0),
        InventoryItem(name="Blood Pressure Monitor", quantity=20, price=100.0),
        InventoryItem(name="Thermometer", quantity=30, price=20.0),
        InventoryItem(name="ECG Machine", quantity=5, price=30000.0),
        InventoryItem(name="Defibrillator", quantity=6, price=20000.0),
        InventoryItem(name="Ventilator", quantity=3, price=50000.0),
        InventoryItem(name="Surgical Instruments", quantity=15, price=1500.0)
    ]
    db.session.bulk_save_objects(inventory_items)
    db.session.commit()

    # Add invoices
    invoices = [
        Invoice(amount=200.0, description="Consultation Fee", patient_id=patients[0].id),
        Invoice(amount=500.0, description="MRI Scan", patient_id=patients[1].id),
        Invoice(amount=300.0, description="X-Ray", patient_id=patients[2].id),
        Invoice(amount=150.0, description="Ultrasound", patient_id=patients[3].id),
        Invoice(amount=50.0, description="Blood Test", patient_id=patients[4].id),
        Invoice(amount=700.0, description="CT Scan", patient_id=patients[5].id),
        Invoice(amount=100.0, description="ECG", patient_id=patients[6].id),
        Invoice(amount=120.0, description="Echocardiogram", patient_id=patients[7].id),
        Invoice(amount=80.0, description="Blood Sugar Test", patient_id=patients[8].id),
        Invoice(amount=250.0, description="Therapy Session", patient_id=patients[9].id)
    ]
    db.session.bulk_save_objects(invoices)
    db.session.commit()

    print("10 records for each entity added successfully!")
