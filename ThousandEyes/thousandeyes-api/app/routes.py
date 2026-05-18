import re

from flask import Blueprint, jsonify, request

from app.thousandeyes_client import ThousandEyesClient, ThousandEyesError

bp = Blueprint("api", __name__)

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _thousandeyes_error_response(exc: ThousandEyesError):
    # Always use 502 for upstream failures so a ThousandEyes 404 ("wrong ID in
    # request") is not mistaken for this service's /adduser route missing.
    return (
        jsonify(
            {
                "error": str(exc),
                "thousandeyes_status": exc.status_code,
                "details": exc.details,
            }
        ),
        502,
    )


def _duplicate_user_error(exc: ThousandEyesError) -> bool:
    if exc.status_code != 400 or not exc.details:
        return False
    if isinstance(exc.details, dict):
        text = " ".join(
            str(exc.details.get(key, ""))
            for key in ("title", "detail", "errorMessage")
        )
    else:
        text = str(exc.details)
    return "already exists" in text.lower()


@bp.get("/health", strict_slashes=False)
def health():
    return jsonify({"status": "ok"})


@bp.get("/showinfo", strict_slashes=False)
def show_info():
    try:
        client = ThousandEyesClient()
        info = client.get_settings_info()
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 500
    except ThousandEyesError as exc:
        return _thousandeyes_error_response(exc)

    return jsonify(info)


@bp.get("/adduser", strict_slashes=False)
def add_user():
    email = request.args.get("email", "").strip()
    name = request.args.get("name", "").strip() or None

    if not email:
        return jsonify({"error": "Missing required query parameter: email"}), 400

    if not EMAIL_PATTERN.match(email):
        return jsonify({"error": "Invalid email address"}), 400

    try:
        client = ThousandEyesClient()
        user = client.create_user(email=email, name=name)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 500
    except ThousandEyesError as exc:
        if _duplicate_user_error(exc):
            try:
                users = client.list_users(account_group_id=client.account_group_id)
            except ThousandEyesError:
                return _thousandeyes_error_response(exc)
            existing = next((user for user in users if user.get("email") == email), None)
            if existing:
                return jsonify({"message": "User already exists", "user": existing}), 200
        return _thousandeyes_error_response(exc)

    return jsonify({"message": "User created", "user": user}), 201
