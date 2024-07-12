from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        # Importing resources within the app context to avoid circular imports
        from app.routes.patient_routes import PatientListResource, PatientResource
        from app.routes.staff_resources import StaffResource, StaffListResource
        from app.routes.inventory_resources import InventoryItemResource, InventoryItemListResource
        from app.routes.billing_resources import InvoiceResource, InvoiceListResource
        from app.routes.insurance_resources import InsuranceClaimListResource

        api = Api(app)

        # Registering resources with Flask-RESTful
        api.add_resource(PatientListResource, '/patients')
        api.add_resource(PatientResource, '/patients/<int:id>')
        api.add_resource(StaffListResource, '/staff')
        api.add_resource(StaffResource, '/staff/<int:id>')
        api.add_resource(InventoryItemListResource, '/inventory/items')
        api.add_resource(InventoryItemResource, '/inventory/items/<int:id>')
        api.add_resource(InvoiceListResource, '/invoices')
        api.add_resource(InsuranceClaimListResource, '/insurance-claims')
        api.add_resource(InvoiceResource, '/invoice/<int:id>')

        # Create database tables based on models
        db.create_all()

    return app
