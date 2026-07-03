from functools import wraps
from flask import session, redirect


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("dni"):
            return redirect("/login")
        return func(*args, **kwargs)
    return wrapper


def cliente_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("dni"):
            return redirect("/login")

        if session.get("role") != "cliente":
            return redirect("/")

        return func(*args, **kwargs)
    return wrapper


def empleado_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("dni"):
            return redirect("/login")

        if session.get("role") != "empleado":
            return redirect("/")

        return func(*args, **kwargs)
    return wrapper