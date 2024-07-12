from flask_restful import Resource, reqparse

from app import db
from app.models.inventory_model import InventoryItem

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Name cannot be blank')
parser.add_argument('quantity', type=int, required=True, help='Quantity cannot be blank')
parser.add_argument('price', type=float, required=True, help='Price cannot be blank')


class InventoryItemResource(Resource):
    def get(self, id):
        item = InventoryItem.query.get_or_404(id)
        return item.to_dict(), 200

    def put(self, id):
        args = parser.parse_args()
        item = InventoryItem.query.get_or_404(id)
        item.name = args.get('name', item.name)
        item.quantity = args.get('quantity', item.quantity)
        item.price = args.get('price', item.price)
        db.session.commit()
        return item.to_dict(), 200

    def delete(self, id):
        item = InventoryItem.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        return '', 204


class InventoryItemListResource(Resource):
    def get(self):
        items = InventoryItem.query.all()
        return [item.to_dict() for item in items], 200

    def post(self):
        args = parser.parse_args()
        new_item = InventoryItem(
            name=args['name'],
            quantity=args['quantity'],
            price=args['price']
        )
        db.session.add(new_item)
        db.session.commit()
        return new_item.to_dict(), 201
