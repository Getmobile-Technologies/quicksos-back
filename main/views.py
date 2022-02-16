from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import MessageSerializer
from drf_yasg.utils import swagger_auto_schema



@swagger_auto_schema("post", request_body=MessageSerializer())
@api_view(["GET","POST"])
def message(request):
    
    if request.method == "GET":
        return Response({"message":"success"}, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response({"message":"success"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error":serializer.errors,"message":"failed"}, status=status.HTTP_400_BAD_REQUEST)
    