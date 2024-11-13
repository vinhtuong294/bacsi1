from django.http import HttpRequest
from rest_framework import viewsets
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .models import UserModel, Role, ERole
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .services import patient_service, doctor_service  # Giả định có các service tương tự
from .repositories import role_repository, user_repository  # Giả định có các repository tương tự
from .serializers import (
    RegisterRequestSerializer,
    UserSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from .services import department_service, patient_service, authenticate_service
from .services.authenticate_service import AuthenticateService
from .services.department_service import DepartmentService


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):

    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        print("Received data: %s", request.data)  # Log dữ liệu nhận được
        return super().create(request, *args, **kwargs)
    # permission_classes = [IsAuthenticated]


def password_reset(request):
    return render(request, 'password_reset/password_reset.html')

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, 'register/register.html')

    def post(self, request):
        serializer = RegisterRequestSerializer(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)

        # Lấy dữ liệu từ serializer
        role_name = serializer.validated_data.get("role")

        print(role_name)

        # Kiểm tra vai trò và gán giá trị tương ứng
        try:
            if role_name is None:
                role = Role.objects.get(name=ERole.PATIENT)
            else:
                role = Role.objects.get(name=role_name)
        except Role.DoesNotExist:
            return Response({"error": "Role not found."}, status=status.HTTP_400_BAD_REQUEST)

        # Tạo người dùng mới
        user = UserModel.objects.create(
            username=serializer.validated_data['username'],
            password=make_password(serializer.validated_data['password']),
            email=serializer.validated_data['email'],
            telephone=serializer.validated_data['telephone'],
            fullname=serializer.validated_data['fullname'],
            birthday=serializer.validated_data['birthday'],
            gender=serializer.validated_data['gender'],
            enabled=True,
            role=role,
        )

        # Lưu người dùng và xử lý tạo đối tượng phụ thuộc vai trò
        user_repository.save(user)

        if role.name == ERole.PATIENT:
            patient_service.create_new_patient(user)
        elif role.name == ERole.DOCTOR:
            doctor_service.create_new_doctor(user)

        # Trả về thông tin xác thực hoặc dữ liệu người dùng
        return Response({
            "username": user.username,
            "role": role.name,
            "message": "User registered successfully."
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, 'login/login.html')

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            # Lấy người dùng từ cơ sở dữ liệu
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # Xác thực mật khẩu
        if user.check_password(password):
            # Sử dụng CustomTokenObtainPairSerializer để tạo token có payload tùy chỉnh
            refresh = RefreshToken.for_user(user)
            # Sử dụng `access_token` từ refresh token có thông tin tùy chỉnh
            access_token = refresh.access_token

            # Thêm thông tin tùy chỉnh vào access token (nếu cần thiết)
            access_token['username'] = user.username
            access_token['email'] = user.email
            if hasattr(user, 'role'):
                access_token['role'] = user.role_id

            # Trả về token cho client
            return Response({
                'access': str(access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)

        # Trả về thông báo lỗi nếu thông tin đăng nhập không chính xác
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


def homepage(request):
    return render(request, 'homepage/homeComponent/homepage.html')

def doctor_homepage(request):
    return render(request, 'doctor_homepage/homedoctor/doctor_homepage.html')

# def home_logged(request):
#     return render(request, 'homepage/homeComponent/homepage.html')


# def admin_homepage(request):
#     return render(request, 'homepage/homeComponent/homepage.html')


# def get_home_page(request):
#     user = authenticate_service.get_user_from_cookie(request)
#     list_department_respones = department_service.get_all_department_responses()
#     context = {
#         "view": "homePage/homeComponent/homePage",
#         "file": "homePage",
#         "listDepartmentRespones": list_department_respones,
#         "user": user,
#     }
#
#     if user is None or user.role == ERole.ADMIN.name:
#         context.update({"nav": "homePage/partials/nav", "navState": "nav"})
#     elif user.role == ERole.DOCTOR.name:
#         context.update({"nav": "homePage/partials/navDoctorLogged", "navState": "navDoctorLogged"})
#     elif user.role == ERole.PATIENT.name:
#         context.update({"nav": "homePage/partials/navLogged", "navState": "navLogged"})
#
#     return render(request, "homePage/index.html", context)
