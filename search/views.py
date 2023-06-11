from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
import os
from search.낱알검색 import pill_scan, find_prescription
from users.models import Prescription, PrescDetail, User
from users.serializers import PrescriptionSerializer


# Create your views here.
class SearchResultListView(generics.ListAPIView):
    def post(self, request):
        if request.FILES.get('image'):
            imageSource = request.FILES['image']
            result = pill_scan(imageSource)
            # file_path = os.path.join(os.path.dirname(__file__), "135273.jpg")
            # file = open(file_path, 'rb')
            # result = pill_scan(file)

            username = request.headers['Username']
            queryset = find_prescription(result, username)
            serializer = PrescriptionSerializer(queryset, many=False)
            print("알약검색 성공")
            print(serializer.data)

        return Response(serializer.data)


