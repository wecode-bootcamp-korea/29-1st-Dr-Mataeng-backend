import json, re, bcrypt

from django.views import View
from django.http  import JsonResponse
from django.conf  import settings

from users.models import User

class SignUpView(View):
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
        REGEX_NAME         = r"^[가-힣]{1,}$"
        REGEX_USERNAME     = r"^[a-zA-Z0-9]{5,}$"
        REGEX_PASSWORD     = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$"
        REGEX_BIRTHDAY     = r"^(19[0-9][0-9]|20\d{2})-(0[0-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$"
        REGEX_EMAIL        = r"^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        REGEX_PHONE_NUMBER = r"^01(?:0|1|[6-9])-(?:\d{3}|\d{4})-\d{4}$"

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

            if not re.match(REGEX_NAME, name):
                return JsonResponse({"message" : "INVALID NAME FORMAT"}, status=400)
            elif not re.match(REGEX_USERNAME, username):
                return JsonResponse({"message" : "INVALID USERNAME FORMAT"}, status=400)
            elif not re.match(REGEX_PASSWORD, password):
                return JsonResponse({"message" : "INVALID PASSWORD FORMAT"}, status=400)
            elif not re.match(REGEX_BIRTHDAY, birthday):
                return JsonResponse({"message" : "INVALID BIRTHDAY FORMAT"}, status=400)
            elif not re.match(REGEX_EMAIL, email):
                return JsonResponse({"message" : "INVALID EMAIL FORMAT"}, status=400)
            elif not re.match(REGEX_PHONE_NUMBER, phone_number):
                return JsonResponse({"message" : "INVALID PHONE_NUMBER FORMAT"}, status=400)
            elif not User.objects.filter(username = recommender).exists():
                return JsonResponse({"message" : "NOT EXIST USERNAME"}, status=400)
            elif User.objects.filter(username = username).exists():
                return JsonResponse({"message" : "USERNAME ALREADY EXIST"}, status=400)

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


class SignInView(View) :
    def post(self, request) :
        try :
            data = json.loads(request.body)

            username    = data['username']
            password = data['password']

            if not User.objects.filter(username=username).exists() :
                return JsonResponse({'message':'INVALID_USER BY USERNAME'}, status=401)

            if not User.objects.filter(password=password).exists() :
                return JsonResponse({'message':'INVALID USER BY PASSWORD'}, status=401)

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError :
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
