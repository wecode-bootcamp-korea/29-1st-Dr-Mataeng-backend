import json, re, bcrypt, jwt

from json.decoder import JSONDecodeError
from django.forms import ValidationError
from django.views import View
from django.http  import JsonResponse
from django.conf  import settings

from users.models import User
from users.utils  import UserValidation

class UserView(View):
    def get(self, request):
        users   = User.objects.all()
        results = []

        for user in users:
            results.append({
                "name"         : user.name,
                "username"     : user.username,
                "password"     : user.password,
                "birthday"     : user.birthday,
                "email"        : user.email,
                "phone_number" : user.phone_number,
                "gender"       : user.gender,
                "recommender"  : user.recommender,
                "created_at"   : user.created_at,
                "updated_at"   : user.updated_at,
            })
        return JsonResponse({'users' : results}, status=200)

    def post(self, request):
        data               = json.loads(request.body)

        try:
            name            = data["name"]
            username        = data["username"]
            password        = data["password"]
            birthday        = data["birthday"]
            email           = data["email"]
            phone_number    = data["phone_number"]
            gender          = data["gender"]
            recommender     = data["recommender"]
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            UserValidation.validate_name(name)
            UserValidation.validate_username(username)
            UserValidation.validate_password(password)
            UserValidation.validate_birthday(birthday)
            UserValidation.validate_email(email)
            UserValidation.validate_phone_number(phone_number)
            UserValidation.exist_username(username)

            user = User(
                name         = name,
                username     = username,
                password     = hashed_password,
                birthday     = birthday,
                email        = email,
                phone_number = phone_number,
                gender       = gender,
                recommender  = recommender,
            )
            user.save()
            return JsonResponse({"message" : "SUCCESS"}, status=201)
        except KeyError: 
            return JsonResponse({"message" : "KeyError"}, status=400)
        except ValidationError as e:
            return JsonResponse({"message" : e.messages}, status=400)
        except JSONDecodeError:
            return JsonResponse({"message": "JSONDECODE ERROR"}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data             = json.loads(request.body)
            username         = data["username"]
            password         = data["password"]
            user             = User.objects.get(username=username)
            encoded_password = user.password.encode('utf-8')

            if bcrypt.checkpw(password.encode("utf-8"), encoded_password):
                access_token = jwt.encode(
                    {"user_id": user.id}, settings.SECRET_KEY, algorithm=settings.ALGORITHMS
                )
                return JsonResponse({
                    "message": "SUCCESS",
                    "access_token": access_token
                }, status=200)
            return JsonResponse({"message": "INVALID_USER(PASSWORD)"}, status=401)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER(USERNAME)"}, status=401)