import json, bcrypt, jwt

from django.db import IntegrityError
from json.decoder import JSONDecodeError
from django.forms import ValidationError
from django.views import View
from django.http  import JsonResponse
from django.conf  import settings

from users.models import User
from users.utils  import (login_decorator,
                          validate_name,
                          validate_username,
                          validate_password,
                          validate_birthday,
                          validate_email,
                          validate_phone_number,
                          exist_username)

class UserView(View):
    @login_decorator
    def get(self, request):
        user = request.user

        results = {
            "name"         : user.name,
            "point"        : user.point,
            "phone_number" : user.phone_number,
            "email"        : user.email
        }

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

            validate_name(name)
            validate_username(username)
            validate_password(password)
            validate_birthday(birthday)
            validate_email(email)
            validate_phone_number(phone_number)
            exist_username(username)

            user = User(
                name         = name,
                username     = username,
                password     = hashed_password,
                birthday     = birthday,
                email        = email,
                phone_number = phone_number,
                gender       = gender,
                recommender  = recommender,
                point        = 1000000
            )
            user.save()
            return JsonResponse({"message" : "SUCCESS"}, status=201)
        except KeyError: 
            return JsonResponse({"message" : "KEY ERROR"}, status=400)
        except ValidationError as e:
            return JsonResponse({"message" : e.messages}, status=400)
        except IntegrityError:
            return JsonResponse({"message" : "USERNAME ALREADY EXIST"}, status=400)
        except JSONDecodeError:
            return JsonResponse({"message" : "JSONDECODE ERROR"}, status=400)

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
                    "message"     : "SUCCESS",
                    "user_id(pk)" : user.id,
                    "access_token": access_token
                }, status=200)
            return JsonResponse({"message": "INVALID_USER(PASSWORD)"}, status=401)
        except KeyError:
            return JsonResponse({"message": "KEY ERROR"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER(USERNAME)"}, status=401)