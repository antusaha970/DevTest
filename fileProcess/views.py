from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomFileSerializer
import pandas as pd


def generate_summary(data):
    summary = data.groupby(['Cust State', 'Cust Pin'])[
        'DPD'].agg(['sum', 'count']).reset_index()
    return summary.to_dict(orient='records')


class FileProcessView(APIView):
    def post(self, request):
        serializer = CustomFileSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.save()
            data = pd.read_excel(file.file.path)
            summary = generate_summary(data)
            return Response(summary)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
