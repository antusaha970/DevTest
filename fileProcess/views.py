from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CustomFileSerializer


class FileProcessView(APIView):
    def post(self, request):
        serializer = CustomFileSerializer(data=request.data)
        if serializer.is_valid():
            return Response("ok")

        return Response(serializer.errors)
