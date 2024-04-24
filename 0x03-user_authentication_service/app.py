#!/usr/bin/env python3
"""Flask app module"""
from auth import Auth
from flask import Flask, jsonify, request, make_response, abort
from flask import url_for, redirect

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


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """login method"""
    if not request.form:
        abort(415)

    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        print(AUTH.valid_login(email, password))
        abort(401)

    id = AUTH.create_session(email)

    resp = make_response({"email": f"{email}", "message": "logged in"})

    resp.set_cookie("session_id", id)

    return resp


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """logout user"""
    session_id = request.cookies.get('session_id')

    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)

    AUTH.destroy_session(user.id)

    return redirect(url_for('index'))


@app.route('/profile', strict_slashes=False)
def profile():
    session_id = request.cookies.get('session_id')

    user = AUTH.get_user_from_session_id(session_id)

    if user:
        return jsonify({"email": f"{user.email}"}), 200

    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """ Get reset password token"""
    email = request.form.get('email')

    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": token})


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """Update password end-point"""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
