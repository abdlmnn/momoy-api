from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Inventory
from .serializers import InventorySerializer
from rest_framework.parsers import MultiPartParser, FormParser

class InventoryView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        inventories = Inventory.objects.all()
        serializer = InventorySerializer(inventories, many=True)
        return Response(serializer.data)

    def post(self, request):
        # By passing request.data to the serializer, we let DRF handle
        # validation and object creation, including the image upload.
        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid():
            # The .save() method will create a new Inventory instance
            # with the validated data, including the uploaded image.
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # If validation fails, the serializer.errors will contain details.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # """Create inventory item"""
        # product_id = request.data.get('product')
        # size = request.data.get('size')
        # price = request.data.get('price')
        # stock = request.data.get('stock')
        # is_new = request.data.get('is_new', False)
        # is_available = request.data.get('is_available', True)
        # image = request.FILES.get('image')

        # # Validate required fields
        # if not all([product_id, size, price, stock]):
        #     return Response({"error": "product, size, price, and stock are required"}, status=status.HTTP_400_BAD_REQUEST)

        # try:
        #     from productAPI.models import Product
        #     product = Product.objects.get(id=product_id)
        # except Product.DoesNotExist:
        #     return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # # Create inventory
        # inventory = Inventory.objects.create(
        #     product=product,
        #     size=size,
        #     price=price,
        #     stock=stock,
        #     is_new=is_new,
        #     is_available=is_available,
        #     image=image,
        # )

        # serializer = InventorySerializer(inventory)
        # return Response(serializer.data, status=status.HTTP_201_CREATED)

class InventoryDetailView(APIView):
    def get(self, request, pk):
        inventory = get_object_or_404(Inventory, pk=pk)
        serializer = InventorySerializer(inventory)
        return Response(serializer.data)

    def put(self, request, pk):
        inventory = get_object_or_404(Inventory, pk=pk)
        serializer = InventorySerializer(inventory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        inventory = get_object_or_404(Inventory, pk=pk)
        inventory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
