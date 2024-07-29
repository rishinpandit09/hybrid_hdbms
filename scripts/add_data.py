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
    doctor1 = Doctor(name="Dr. Alice Smith", specialty="Cardiology")
    doctor2 = Doctor(name="Dr. Bob Johnson", specialty="Neurology")
    doctor3 = Doctor(name="Dr. Carol Lee", specialty="Orthopedics")
    doctor4 = Doctor(name="Dr. David Kim", specialty="Dermatology")
    doctor5 = Doctor(name="Dr. Eva Green", specialty="Pediatrics")
    doctor6 = Doctor(name="Dr. Frank Brown", specialty="Oncology")
    doctor7 = Doctor(name="Dr. Grace White", specialty="Gastroenterology")
    doctor8 = Doctor(name="Dr. Henry Black", specialty="Urology")
    doctor9 = Doctor(name="Dr. Irene Blue", specialty="Endocrinology")
    doctor10 = Doctor(name="Dr. Jack Grey", specialty="Psychiatry")

    db.session.add_all([doctor1, doctor2, doctor3, doctor4, doctor5, doctor6, doctor7, doctor8, doctor9, doctor10])
    db.session.commit()

    # Add patients
    patient1 = Patient(name="John Doe", age=45, diagnosis="Heart Disease", treatment="Medication", doctor_id=doctor1.id)
    patient2 = Patient(name="Jane Roe", age=50, diagnosis="Brain Tumor", treatment="Surgery", doctor_id=doctor2.id)
    patient3 = Patient(name="Jake Paul", age=35, diagnosis="Fracture", treatment="Cast", doctor_id=doctor3.id)
    patient4 = Patient(name="Lily Evans", age=28, diagnosis="Eczema", treatment="Ointment", doctor_id=doctor4.id)
    patient5 = Patient(name="Harry Potter", age=10, diagnosis="Asthma", treatment="Inhaler", doctor_id=doctor5.id)
    patient6 = Patient(name="Sam Wilson", age=55, diagnosis="Lung Cancer", treatment="Chemotherapy", doctor_id=doctor6.id)
    patient7 = Patient(name="Mary Jane", age=60, diagnosis="Ulcer", treatment="Antacids", doctor_id=doctor7.id)
    patient8 = Patient(name="Peter Parker", age=40, diagnosis="Kidney Stones", treatment="Surgery", doctor_id=doctor8.id)
    patient9 = Patient(name="Tony Stark", age=50, diagnosis="Diabetes", treatment="Insulin", doctor_id=doctor9.id)
    patient10 = Patient(name="Bruce Wayne", age=35, diagnosis="Depression", treatment="Therapy", doctor_id=doctor10.id)

    db.session.add_all([patient1, patient2, patient3, patient4, patient5, patient6, patient7, patient8, patient9, patient10])
    db.session.commit()

    # Add employees
    employee1 = Employee(name="Alice Johnson", role="Nurse", department="Cardiology")
    employee2 = Employee(name="Bob Smith", role="Technician", department="Neurology")
    employee3 = Employee(name="Charlie Brown", role="Receptionist", department="Orthopedics")
    employee4 = Employee(name="David Williams", role="Pharmacist", department="Dermatology")
    employee5 = Employee(name="Eve Davis", role="Nurse", department="Pediatrics")
    employee6 = Employee(name="Frank Thomas", role="Technician", department="Oncology")
    employee7 = Employee(name="Grace Martin", role="Receptionist", department="Gastroenterology")
    employee8 = Employee(name="Henry Jackson", role="Pharmacist", department="Urology")
    employee9 = Employee(name="Irene Lee", role="Nurse", department="Endocrinology")
    employee10 = Employee(name="Jack Harris", role="Technician", department="Psychiatry")

    db.session.add_all([employee1, employee2, employee3, employee4, employee5, employee6, employee7, employee8, employee9, employee10])
    db.session.commit()

    # Add insurance claims
    claim1 = InsuranceClaim(patient_id=patient1.id, amount=5000.0, status="Approved")
    claim2 = InsuranceClaim(patient_id=patient2.id, amount=10000.0, status="Pending")
    claim3 = InsuranceClaim(patient_id=patient3.id, amount=3000.0, status="Denied")
    claim4 = InsuranceClaim(patient_id=patient4.id, amount=4000.0, status="Approved")
    claim5 = InsuranceClaim(patient_id=patient5.id, amount=2000.0, status="Pending")
    claim6 = InsuranceClaim(patient_id=patient6.id, amount=15000.0, status="Approved")
    claim7 = InsuranceClaim(patient_id=patient7.id, amount=8000.0, status="Denied")
    claim8 = InsuranceClaim(patient_id=patient8.id, amount=6000.0, status="Approved")
    claim9 = InsuranceClaim(patient_id=patient9.id, amount=7000.0, status="Pending")
    claim10 = InsuranceClaim(patient_id=patient10.id, amount=5000.0, status="Approved")

    db.session.add_all([claim1, claim2, claim3, claim4, claim5, claim6, claim7, claim8, claim9, claim10])
    db.session.commit()

    # Add inventory items
    item1 = InventoryItem(name="Stethoscope", quantity=10, price=50.0)
    item2 = InventoryItem(name="MRI Machine", quantity=2, price=100000.0)
    item3 = InventoryItem(name="X-Ray Machine", quantity=3, price=75000.0)
    item4 = InventoryItem(name="Ultrasound Machine", quantity=4, price=50000.0)
    item5 = InventoryItem(name="Blood Pressure Monitor", quantity=20, price=100.0)
    item6 = InventoryItem(name="Thermometer", quantity=30, price=20.0)
    item7 = InventoryItem(name="ECG Machine", quantity=5, price=30000.0)
    item8 = InventoryItem(name="Defibrillator", quantity=6, price=20000.0)
    item9 = InventoryItem(name="Ventilator", quantity=3, price=50000.0)
    item10 = InventoryItem(name="Surgical Instruments", quantity=15, price=1500.0)

    db.session.add_all([item1, item2, item3, item4, item5, item6, item7, item8, item9, item10])
    db.session.commit()

    # Add invoices
    invoice1 = Invoice(amount=200.0, description="Consultation Fee", patient_id=patient1.id)
    invoice2 = Invoice(amount=500.0, description="MRI Scan", patient_id=patient2.id)
    invoice3 = Invoice(amount=300.0, description="X-Ray", patient_id=patient3.id)
    invoice4 = Invoice(amount=150.0, description="Ultrasound", patient_id=patient4.id)
    invoice5 = Invoice(amount=50.0, description="Blood Test", patient_id=patient5.id)
    invoice6 = Invoice(amount=700.0, description="CT Scan", patient_id=patient6.id)
    invoice7 = Invoice(amount=100.0, description="ECG", patient_id=patient7.id)
    invoice8 = Invoice(amount=120.0, description="Echocardiogram", patient_id=patient8.id)
    invoice9 = Invoice(amount=80.0, description="Blood Sugar Test", patient_id=patient9.id)
    invoice10 = Invoice(amount=250.0, description="Therapy Session", patient_id=patient10.id)

    db.session.add_all([invoice1, invoice2, invoice3, invoice4, invoice5, invoice6, invoice7, invoice8, invoice9, invoice10])
    db.session.commit()

    print("10 records for each entity added successfully!")
