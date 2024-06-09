#!/usr/bin/env python3
"""Session views
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User
from os import getenv
from typing import Dict


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Dict:
    """return JSON representation of authenticated user.
    """
    from api.v1.app import auth

    email = request.form.get('email')
    password = request.form.get('password')
    session = getenv("SESSION_NAME")

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})

    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user[0].id)
    json_resp = jsonify(user[0].to_json())
    json_resp.set_cookie(session, session_id)

    return json_resp


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout() -> Dict:
    """logout user.
    """
    from api.v1.app import auth

    if not auth.session_cookie(request):
        abort(401)
    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200
