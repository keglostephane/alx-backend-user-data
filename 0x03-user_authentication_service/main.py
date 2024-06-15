#!/usr/bin/env python3
"""Test module
"""
import requests


def register_user(email: str, password: str) -> None:
    """new user registration"""
    url = 'http://0.0.0.0:5000/users/'
    data = {"email": email, "password": password}
    resp = requests.post(url, data=data)
    assert resp.status_code == 200
    assert resp.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """log in with wrong password"""
    url = 'http://0.0.0.0:5000/sessions/'
    data = {"email": email, "password": password}
    resp = requests.post(url, data)
    assert resp.status_code == 401


def log_in(email: str, password: str) -> str:
    """login with right credentials"""
    url = 'http://0.0.0.0:5000/sessions/'
    data = {"email": email, "password": password}
    resp = requests.post(url, data)
    assert resp.status_code == 200
    assert resp.json() == {"email": email, "message": "logged in"}
    session_id = resp.cookies.get('session_id')
    assert session_id is not None
    return session_id


def profile_unlogged() -> None:
    """get profile when logged out"""
    url = "http://0.0.0.0:5000/profile/"
    resp = requests.get(url)
    assert resp.status_code == 403


def profile_logged(session_id: str) -> None:
    """get profile when logged in"""
    url = 'http://0.0.0.0:5000/profile/'
    cookies = {"session_id": session_id}
    resp = requests.get(url, cookies=cookies)
    assert resp.status_code == 200
    assert resp.json() == {"email": "guillaume@holberton.io"}


def log_out(session_id: str) -> None:
    """log out"""
    url = 'http://0.0.0.0:5000/sessions/'
    index = 'http://0.0.0.0:5000/'
    cookies = {"session_id": session_id}
    resp = requests.delete(url, cookies=cookies)
    assert resp.status_code == 200
    assert resp.url == index


def reset_password_token(email: str) -> str:
    """password request modification"""
    url = 'http://0.0.0.0:5000/reset_password/'
    data = {"email": email}
    resp = requests.post(url, data=data)
    assert resp.status_code == 200
    reset_token = resp.json().get('reset_token')
    assert resp.json() == {"email": email, "reset_token": reset_token}
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """modify password after password request modification"""
    url = 'http://0.0.0.0:5000/reset_password/'
    data = {"email": email,
            "reset_token": reset_token,
            "new_password": new_password}
    resp = requests.put(url, data=data)
    assert resp.status_code == 200
    assert resp.json() == {"email": email, "message": "Password updated"}


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
