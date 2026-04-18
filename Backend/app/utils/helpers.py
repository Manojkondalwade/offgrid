from flask import jsonify


def success(data=None, message='Success', code=200):
    """Standard success response."""
    resp = {'success': True, 'message': message}
    if data is not None:
        resp['data'] = data
    return jsonify(resp), code


def error(message='An error occurred', code=400):
    """Standard error response."""
    return jsonify({'success': False, 'error': message}), code


def validate_required(data: dict, fields: list):
    """Returns list of missing required fields."""
    return [f for f in fields if not data.get(f)]
