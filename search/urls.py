from django.urls import path
from . import views

urlpatterns = [
    path('result/', views.SearchResultListView.as_view())
]