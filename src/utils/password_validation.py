from rest_framework.serializers import ValidationError
import re

def validate_password(password):

    if len(password) < 8 or len(password) > 30:
        raise ValidationError("Password must be between 8 and 30 characters.")

    if not re.search(r"[A-Z]", password):
        raise ValidationError("Password must contain at least one uppercase letter.")

    if not re.search(r"[a-z]", password):
        raise ValidationError("Password must contain at least one lowercase letter.")

    if not re.search(r"[0-9]", password):
        raise ValidationError("Password must contain at least one digit.")

    if " " in password:
        raise ValidationError("Password must not contain spaces.")

    if not re.match(r"^[a-zA-Z0-9]+$", password):
        raise ValidationError("Password must contain only Latin letters and digits.")

    return password
