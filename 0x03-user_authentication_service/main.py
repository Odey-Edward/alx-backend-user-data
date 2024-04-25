#!/usr/bin/env python3
"""Main Module wit End-to-end integration test"""
import requests


def register_user(EMAIL: str, PASSWD: str) -> None:
    """register a new user"""
    expected_data = {"email": EMAIL, "message": "user created"}

    data = {'email': EMAIL, 'password': PASSWD}

    resp = requests.post('http://localhost:5000/users', data=data)

    actual_data = resp.json()

    assert resp.status_code == 200
    assert expected_data == actual_data


def log_in_wrong_password(EMAIL: str, NEW_PASSWD: str) -> None:
    """test for user login with wrong credential"""

    data = {'email': EMAIL, 'password': NEW_PASSWD}

    resp = requests.post('http://localhost:5000/sessions', data=data)

    assert resp.status_code == 401


def profile_unlogged() -> None:
    """test for user profile retrival without a
    session_id"""
    resp = requests.get('http://localhost:5000/profile')

    assert resp.status_code == 403


def log_in(email: str, password: str) -> str:
    """test for user logs in with correct credentials"""
    expected_data = {"email": email, "message": "logged in"}

    data = {'email': email, 'password': password}

    resp = requests.post('http://localhost:5000/sessions', data=data)

    actual_data = resp.json()

    assert resp.status_code == 200
    assert expected_data == actual_data
    assert resp.cookies.get('session_id')

    return resp.cookies.get('session_id')


def profile_logged(session_id: str) -> None:
    """get user profile with cookies set"""
    cookie = dict(session_id=session_id)
    expected_data = {"email": "guillaume@holberton.io"}

    resp = requests.get('http://localhost:5000/profile', cookies=cookie)

    actual_data = resp.json()

    assert resp.status_code == 200
    assert expected_data == actual_data


def log_out(session_id: str) -> None:
    """logout a user"""

    cookie = dict(session_id=session_id)

    resp = requests.delete('http://localhost:5000/sessions', cookies=cookie)

    assert resp.status_code == 200


def reset_password_token(email: str) -> str:
    """get password reset token"""
    data = dict(email=email)

    resp = requests.post('http://localhost:5000/reset_password', data=data)

    assert resp.status_code == 200
    assert resp.json()

    return resp.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """reset user password with the reset_token"""
    expected_data = {"email": email, "message": "Password updated"}

    data = dict(email=email, reset_token=reset_token,
                new_password=new_password)

    resp = requests.put('http://localhost:5000/reset_password', data=data)

    assert resp.status_code == 200
    assert resp.json()
    assert resp.json() == expected_data


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
