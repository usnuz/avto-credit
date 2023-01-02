from .serializer import *
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def credit(request):
    c = Credit.objects.all()
    ser = CreditSerializer(c, many=True)
    return Response(ser.data)
