from django.urls import path

from users.views import UserView,SignInView

urlpatterns = [
    path("/user", UserView.as_view()),
    path("/signin", SignInView.as_view())
]