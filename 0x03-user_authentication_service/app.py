#!/usr/bin/env python3
"""Flask App
"""
from flask import Flask, jsonify, request, abort, 
from auth import Auth
from typing import Dict

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome() -> Dict:
    """Index
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> Dict:
    """User Registration
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": user.email, "message": "user created"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> Dict:
    """Log in a user.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(404)

    session_id = AUTH.create_session(email)
    resp = jsonify({"email": email, "message": "logged in"})
    resp.set_cookie('session_id', session_id)

    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
