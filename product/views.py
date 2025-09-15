from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *

class TypeView(APIView):
  
  def get(self, request, format=None):
    try:
      types = Type.objects.all()
      serializer = TypeSerializer(types, many=True)
      return Response({
        "data": serializer.data,
        "status" : 200,
      })
    except Type.DoesNotExist:
      return Response({
        "error": "Types not found",
        "status" : 404,
      })
    except Exception as e:
      return Response({
        "error": str(e),
        "status" : 500,
      })
  
  def post(self, request, format=None):
    serializer = TypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": f"{serializer.data['name']} created successfully"},
            status=200
        )
    return Response(serializer.errors, status=400)
  
  def put(self, request, format=None):
    return Response({"message": "Put is working"}, status=200)
  
class ProductView(APIView):
  
  def get(self, request, format=None):

   return Response("This is Product")
  
class InventoryView(APIView):
  
  def get(self, request, format=None):

    return Response("This is Inventory")
