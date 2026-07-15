"""
Validadores genericos reutilizables por los servicios de cada entidad.
"""
import re

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class ValidationError(Exception):
    """Excepcion levantada cuando un payload no cumple las reglas de negocio."""

    def __init__(self, errors):
        if isinstance(errors, str):
            errors = [errors]
        self.errors = errors
        super().__init__("; ".join(errors))


def require_fields(payload: dict, fields: list):
    missing = [
        f for f in fields
        if payload.get(f) is None or (isinstance(payload.get(f), str) and not payload.get(f).strip())
    ]
    if missing:
        raise ValidationError([f"El campo '{f}' es obligatorio." for f in missing])


def validate_string(payload: dict, field: str, min_len=1, max_len=255, required=True):
    value = payload.get(field)
    if value is None:
        if required:
            raise ValidationError(f"El campo '{field}' es obligatorio.")
        return None
    if not isinstance(value, str):
        raise ValidationError(f"El campo '{field}' debe ser una cadena de texto.")
    value = value.strip()
    if len(value) < min_len or len(value) > max_len:
        raise ValidationError(
            f"El campo '{field}' debe tener entre {min_len} y {max_len} caracteres."
        )
    return value


def validate_int(payload: dict, field: str, required=True, min_value=None, max_value=None):
    value = payload.get(field)
    if value is None:
        if required:
            raise ValidationError(f"El campo '{field}' es obligatorio.")
        return None
    try:
        value = int(value)
    except (TypeError, ValueError):
        raise ValidationError(f"El campo '{field}' debe ser un numero entero.")
    if min_value is not None and value < min_value:
        raise ValidationError(f"El campo '{field}' debe ser mayor o igual a {min_value}.")
    if max_value is not None and value > max_value:
        raise ValidationError(f"El campo '{field}' debe ser menor o igual a {max_value}.")
    return value


def validate_email(payload: dict, field: str = "correo", required=True):
    value = payload.get(field)
    if value is None:
        if required:
            raise ValidationError(f"El campo '{field}' es obligatorio.")
        return None
    value = value.strip().lower()
    if not EMAIL_REGEX.match(value):
        raise ValidationError(f"El campo '{field}' no tiene un formato de correo valido.")
    return value


def validate_choice(payload: dict, field: str, choices: list, required=True, default=None):
    value = payload.get(field, default)
    if value is None:
        if required:
            raise ValidationError(f"El campo '{field}' es obligatorio.")
        return default
    if value not in choices:
        raise ValidationError(f"El campo '{field}' debe ser uno de: {', '.join(choices)}.")
    return value
