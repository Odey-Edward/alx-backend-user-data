#!/usr/bin/env python3
"""Flask app module"""
from auth import Auth
from flask import Flask, jsonify, request

app = Flask(__name__)

AUTH = Auth()


@app.route('/')
def index():
    """home endpiont"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """register and return information on the user"""
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": f"{email}", "message": "user created"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
