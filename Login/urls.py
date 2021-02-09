from django.urls import path
from . import views

app_name = "Login"  # For Relative url

urlpatterns = [
    path('signup/',views.signUp,name="signup"),
    path('login/',views.loginUser,name="login")
]
