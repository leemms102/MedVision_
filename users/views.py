import django.db.utils
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User as AuthUser
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Prescription, DrugInfo
from .serializers import UserSerializer, PrescriptionSerializer, DrugInfoSerializer
from rest_framework import generics, status
# from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
class LoginView(APIView):
    """
      API View for login through a POST request.
      """
    def post(self, request):
        username = request.data.get('id')
        password = request.data.get('password')
        loginUser = UserAuth.authenticate(userId=username, userPassword=password)

        if loginUser is not None:
            print('로그인 성공')
            user = authenticate(username=username, password=password)
            login(request, user=user)
            serializer = UserSerializer(loginUser)
            print(request.user)
            print(request.headers)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "아이디 또는 비밀번호가 틀립니다."}, status=status.HTTP_401_UNAUTHORIZED)

class UserAuth:
    def authenticate(userId=None, userPassword=None):
        try:
            user = User.objects.get(userId=userId)
            if userPassword == user.userPassword:
                return user
        except User.DoesNotExist:
            return None

class RegisterView(APIView):
    """
      API View to create or get a list of all the registered
      users. GET request returns the registered users whereas
      a POST request allows to create a new user.
      """
    def get(self, format=None):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        username = request.data.get('id')
        password = request.data.get('password')
        email = request.data.get('email')
        try:
            createUser = User(userId=username, userPassword=password, userEmail=email)
            createUser.save()
            AuthUser(username=username, password=password).save()
        except django.db.utils.IntegrityError as e:
            if 'userId' in e.args[0]:
                print("아이디가 이미 사용중입니다!")
            if 'userEmail' in e.args[0]:
                print("이메일이 이미 사용중입니다!")
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        loginUser = UserAuth.authenticate(userId=username, userPassword=password)
        if loginUser is not None:
            user = authenticate(username=username, password=password)
            login(request, user=user)
            print(f"{user}님! 회원가입을 축하합니다")
            login(request, user=user, backend='users.views.UserAuth')
            serializer = UserSerializer(loginUser)
            return Response(serializer.data, status=status.HTTP_200_OK)

class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PrescriptionView(generics.ListCreateAPIView):

    def get(self, request):
        # 로그인된 사용자 정보 가져오기
        userId = User.objects.get(userId=request.user)
        print(userId.userId)
        # Serializer에서 해당 사용자의 정보 검색
        queryset = Prescription.objects.filter(userId=userId)

        # Serializer를 사용하여 응답 데이터 직렬화
        serializer = PrescriptionSerializer(queryset, many=True)
        return Response(serializer.data)

class DrugInfoView(generics.ListCreateAPIView):
    queryset = DrugInfo.objects.all()
    serializer_class = DrugInfoSerializer

"""
  login via web 
  """
def index(request):
    if request.method == 'GET':
        print('Start MedVision')
        return render(request, 'login.html')

    elif request.method == 'POST':
        id = request.POST.get('id')
        password = request.POST.get('password')

        res_data = {}

        if not (id and password):
            res_data['error'] = '아이디 또는 비밀번호를 입력하세요'
        else:
            loginUser = User.objects.get(userId=id)
            if password == loginUser.userPassword:
                request.session['userId'] = id
                return redirect('/api/authenticate')
            else: res_data['error'] = '비밀번호를 다시 입력하세요'

        return render(request, 'login.html', res_data)

