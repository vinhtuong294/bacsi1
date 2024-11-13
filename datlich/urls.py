from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from . import views

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    path('password-reset/',views.password_reset, name="password_reset"),
    path('homepage/',homepage,name='homepage'),
    path('doctor_homepage/', doctor_homepage, name='doctor_homepage'),
    # path('home_logged/', home_logged, name='home_logged'),
    # path('home', views.get_home_page, name='home'),,

]
