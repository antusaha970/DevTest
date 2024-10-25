from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomFileSerializer
import pandas as pd
from django.core.mail import send_mail


def generate_summary(data):
    summary = data.groupby(['Cust State', 'Cust Pin'])[
        'DPD'].agg(['sum', 'count']).reset_index()
    summary = summary.rename(
        columns={'sum': 'Total DPD', 'count': 'Count of Records'})
    return summary.to_dict(orient='records')


def send_summary_mail(summary):
    message = "Summary Report:\n\n"
    message += "{}\t {}\t {}\t {}\n".format("Cust State",
                                            "Cust Pin", "Total DPD", 'Count of Records')
    message += "-" * 80 + "\n"
    for row in summary:
        message += "{}\t {}\t {}\t {}\n".format(
            row['Cust State'], row['Cust Pin'], row['Total DPD'], row['Count of Records'])

    send_mail('Python Assignment - Antu Saha', message,
              'antu.digi.88@gmail.com', ['tech@themedius.ai'])


class FileProcessView(APIView):
    def post(self, request):
        serializer = CustomFileSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.save()
            data = pd.read_excel(file.file.path)
            summary = generate_summary(data)
            send_summary_mail(summary)
            return Response(summary)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
