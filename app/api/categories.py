from flask import request, jsonify, url_for
from app import db
from app.api import bp
from app.api.errors import bad_request
from app.models import Category, Sensor

@bp.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json() or {}
    if 'name' not in data:
        return bad_request('must include name field')
    if 'units' not in data:
        return bad_request('must include units field')
    if Category.query.filter_by(name=data['name']).first():
        return bad_request('please use a different name')
    category = Category()
    category.from_dict(data)
    db.session.add(category)
    db.session.commit()
    response = jsonify(category.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_category', category_id=category.id)
    return response

@bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    data = Category.query.get_or_404(category_id).to_dict()
    return jsonify(data)

@bp.route('/categories', methods=['GET'])
def get_categories():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 25)
    data = Category.to_collection_dict(Category.query, page, per_page,
        'api.get_categories')
    return jsonify(data)

@bp.route('/sensors/<int:sensor_id>/categories', methods=['GET'])
def get_categories_of_sensor(sensor_id):
    sensor = Sensor.query.get_or_404(sensor_id)
    return jsonify({
        'items': [category.to_dict() for category in sensor.categories],
        '_meta': {
            'total_items': len(sensor.categories)
        }
    })

@bp.route('/sensors/<int:sensor_id>/categories/add', methods=['PATCH'])
def add_categories_to_sensor(sensor_id):
    data = request.get_json() or {}
    if 'categories' not in data:
        return bad_request('must include categories field')
    sensor = Sensor.query.get_or_404(sensor_id)
    sensor.add_categories(data)
    db.session.add(sensor)
    db.session.commit()
    response = jsonify()
    response.status_code = 204
    response.headers['Location'] = url_for('api.get_categories_of_sensor', sensor_id=sensor.id)
    return response

@bp.route('/sensors/<int:sensor_id>/categories/remove', methods=['PATCH'])
def remove_categories_from_sensor(sensor_id):
    data = request.get_json() or {}
    if 'categories' not in data:
        return bad_request('must include categories field')
    sensor = Sensor.query.get_or_404(sensor_id)
    sensor.remove_categories(data)
    db.session.add(sensor)
    db.session.commit()
    response = jsonify()
    response.status_code = 204
    response.headers['Location'] = url_for('api.get_categories_of_sensor', sensor_id=sensor.id)
    return response