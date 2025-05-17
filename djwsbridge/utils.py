# djwsbridge/utils.py
from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get_chat_model():
    model_path = getattr(settings, "DJWSBRIDGE_CHAT_MODEL", None)
    if not model_path:
        raise ImproperlyConfigured("DJWSBRIDGE_CHAT_MODEL is not defined in settings.")
    return apps.get_model(model_path)


def get_message_model():
    model_path = getattr(settings, "DJWSBRIDGE_MESSAGE_MODEL", None)
    if not model_path:
        raise ImproperlyConfigured("DJWSBRIDGE_MESSAGE_MODEL is not defined in settings.")
    return apps.get_model(model_path)


def filter_valid_fields(model_class, data: dict) -> dict:
    field_names = {f.name for f in model_class._meta.get_fields()}
    filtered_data = {k: v for k, v in data.items() if k in field_names}
    invalid_keys = set(data.keys()) - field_names

    if invalid_keys:
        raise ValueError(f"Invalid fields for model {model_class.__name__}: {', '.join(invalid_keys)}")
    return filtered_data
