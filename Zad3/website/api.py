from flask import Blueprint, jsonify, request
from .website import DataClass
from . import db

api = Blueprint('api', __name__)


@api.route('/api/data', methods=['GET', 'POST'])
def api_data():
    if request.method == 'GET':
        data = DataClass.query.order_by(DataClass.category).all()
        data_list = [{'id': point.uid, 'feature1': point.feature1, 'feature2': point.feature2,
                      'category': point.category} for point in data]
        return jsonify(data_list)
    elif request.method == 'POST':
        try:
            data = request.json
            if data['feature1'].isdigit() and data['feature2'].isdigit() and data['category'].isdigit():
                new_data = DataClass(feature1=float(data['feature1']), feature2=float(data['feature2']),
                                     category=int(data['category']))
                db.session.add(new_data)
                db.session.commit()
                return jsonify({'id': new_data.uid}), 201
            else:
                return jsonify({'error': 'Invalid data'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500


@api.route('/api/data/<int:uid>', methods=['DELETE'])
def delete_data(uid):
    try:
        deleted_data = DataClass.query.get(uid)
        if deleted_data:
            db.session.delete(deleted_data)
            db.session.commit()
            return jsonify({'uid': uid}), 200
        else:
            return jsonify({'error': 'Record not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    