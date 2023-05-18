from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.LoginView.as_view(), name='users'),
    path('user/', views.UserView.as_view()),
    path('prescription/', views.PrescriptionView.as_view()),
    path('druginfo/', views.DrugInfoView.as_view()),
    path('signup/', views.RegisterView.as_view()),
    # path('schedules/', views.scheduleList),
]