from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Product
from .serializers import ProductSerializer

class ProductView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailView(APIView):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductSearchView(APIView):
    def get(self, request):
        queryset = Product.objects.all()

        # Search by name or description
        search = request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )

        # Filter by category
        category = request.query_params.get('category', '')
        if category:
            queryset = queryset.filter(category__name__icontains=category)

        # Filter by category ID
        category_id = request.query_params.get('category_id', '')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Filter by is_new
        is_new = request.query_params.get('is_new', '')
        if is_new.lower() in ['true', '1', 'yes']:
            queryset = queryset.filter(is_new=True)
        elif is_new.lower() in ['false', '0', 'no']:
            queryset = queryset.filter(is_new=False)

        # Order by (default: newest first)
        order_by = request.query_params.get('order_by', '-created_at')
        if order_by in ['name', '-name', 'created_at', '-created_at', 'category__name']:
            queryset = queryset.order_by(order_by)

        serializer = ProductSerializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })
