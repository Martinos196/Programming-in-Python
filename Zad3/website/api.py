from flask import jsonify, Blueprint, request
from .website import DataPoint
from . import db


# fun sprawdzajaca czy wartosc moze byc zmieniona na float
def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


# tworzenie blueprint dla flask
api = Blueprint('api', __name__)


# def trasy dla endpointu
@api.route('/api/data', methods=['GET', 'POST'])
def api_data():
    if request.method == 'GET':
        data = DataPoint.query.order_by(DataPoint.uid).all()
        data_list = [{'id': point.uid, 'feature1': point.feature1, 'feature2': point.feature2,
                      'category': point.category} for point in data]
        return jsonify(data_list)
    elif request.method == 'POST':
        data = request.json
        # sprawdzenie czy dane wejsciowe sa float
        if is_float(data['feature1']) and is_float(data['feature2']) and data['category'].isdigit():
            new_data = DataPoint(feature1=float(data['feature1']), feature2=float(data['feature2']),
                                 category=int(data['category']))
            db.session.add(new_data)
            db.session.commit()
            return jsonify({'id': new_data.uid}), 201
        else:
            return jsonify({'error': 'Invalid data'}), 400


# def. trasy dla endpointu obslugujacej metode delete
@api.route('/api/data/<int:uid>', methods=['DELETE'])
def delete_data(uid):
    deleted_data = DataPoint.query.get(uid)
    if deleted_data:
        db.session.delete(deleted_data)
        db.session.commit()
        return jsonify({'uid': uid}), 200
    else:
        return jsonify({'error': 'Not found'}), 404
    