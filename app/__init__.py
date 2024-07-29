# app/__init__.py
import logging
from flask import Flask
from flask_migrate import Migrate
from neo4j import GraphDatabase

# from gqlalchemy import Memgraph
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

from app.db import db
from app.routes.graph_creation_route import CreateGraphInMemgraph
from app.routes.graph_route import GraphRepresentationResource
from app.routes.patient_graph import PatientGraph
from app.schema import schema





# Define correct URI and AUTH arguments (no AUTH by default)
URI = "bolt://localhost:7687"
AUTH = ("", "")
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    with GraphDatabase.driver(URI, auth=AUTH) as client:
        # Check the connection
        client.verify_connectivity()
    db.init_app(app)

    migrate = Migrate(app, db)

    with app.app_context():
        # Importing resources within the app context to avoid circular imports
        from app.routes.patient_routes import PatientListResource, PatientResource
        # from app.routes.graph_patient_route import GraphPatientListResource, GraphPatientResource
        from app.routes.staff_resources import StaffResource, StaffListResource
        from app.routes.inventory_resources import InventoryItemResource, InventoryItemListResource
        from app.routes.billing_resources import InvoiceResource, InvoiceListResource
        from app.routes.insurance_resources import InsuranceClaimListResource

        api = Api(app)

        # Registering resources with Flask-RESTful
        api.add_resource(PatientListResource, '/patients')
        api.add_resource(PatientResource, '/patients/<int:id>')
        # api.add_resource(GraphPatientListResource, '/graph/patients')
        # api.add_resource(GraphPatientResource, '/graph/patients/<int:id>')
        api.add_resource(StaffListResource, '/staff')
        api.add_resource(StaffResource, '/staff/<int:id>')
        api.add_resource(InventoryItemListResource, '/inventory/items')
        api.add_resource(InventoryItemResource, '/inventory/items/<int:id>')
        api.add_resource(InvoiceListResource, '/invoices')
        api.add_resource(InsuranceClaimListResource, '/insurance-claims')
        api.add_resource(InvoiceResource, '/invoice/<int:id>')
        api.add_resource(GraphRepresentationResource, '/graph')
        api.add_resource(CreateGraphInMemgraph, '/create-graph')  # Register the graph creation route
        from flask_graphql import GraphQLView
        api.add_resource(PatientGraph, '/patient-graph')  # Register the patient graph route

        app.add_url_rule(
            '/graphql',
            view_func=GraphQLView.as_view(
                'graphql',
                schema=schema,
                graphiql=True  # Enable GraphiQL interface
            )
        )

        @app.before_first_request
        def create_tables():
            db.create_all()
        # Create database tables based on models
        db.create_all()

    return app
