from django.core.exceptions import ValidationError


def validate_price(value):
    if value < 0:
        raise ValidationError("The price can not be a negative value")
