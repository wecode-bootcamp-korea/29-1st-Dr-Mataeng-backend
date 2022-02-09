import json, jwt, re

from django.http            import JsonResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.utils        import IntegrityError
from django.conf            import settings

from users.models  import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get("Authorization")
            payload      = jwt.decode(access_token, settings.SECRET_KEY, algorithms = settings.ALGORITHMS)
            user         = User.objects.get(id = payload['user_id'])
            request.user = user
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message' : 'INVALID_TOKEN' }, status=401)
        except User.DoesNotExitst:
            return JsonResponse({'message' : 'INVALID_USER'}, status=401)
        return func(self, request, *args, **kwargs)
    return wrapper

def validate_name(name):
    REGEX_NAME = r"^[가-힣]{1,}$"

    if not re.match(REGEX_NAME, name):
        raise ValidationError("INVALID NAME FORMAT")

def validate_username(username):
    REGEX_USERNAME = r"^[a-zA-Z0-9]{5,}$"

    if not re.match(REGEX_USERNAME, username):
        raise ValidationError("INVALID USERNAME FORMAT")

def validate_password(password):
    REGEX_PASSWORD = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$"

    if not re.match(REGEX_PASSWORD, password):
        raise ValidationError("INVALID PASSWORD FORMAT")

def validate_birthday(birthday):
    REGEX_BIRTHDAY = r"^(19[0-9][0-9]|20\d{2})-(0[0-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$"

    if not re.match(REGEX_BIRTHDAY, birthday):
        raise ValidationError("INVALID BIRTHDAY FORMAT")

def validate_email(email):
    REGEX_EMAIL = r"^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if not re.match(REGEX_EMAIL, email):
        raise ValidationError("INVALID EMAIL FORMAT")

def validate_phone_number(phone_number):
    REGEX_PHONE_NUMBER = r"^01(?:0|1|[6-9])-(?:\d{3}|\d{4})-\d{4}$"

    if not re.match(REGEX_PHONE_NUMBER, phone_number):
        raise ValidationError("INVALID PHONE_NUMBER FORMAT")

def exist_username(username):
    if User.objects.filter(username = username).exists():
        raise IntegrityError