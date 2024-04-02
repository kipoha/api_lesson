from rest_framework.decorators import api_view
from rest_framework.response import Response
from product import serializers, models
from rest_framework import status
from django.db.models import Count
from rest_framework.generics import *
from rest_framework.pagination import *

class CategoryListAPI(ListCreateAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    pagination_class = PageNumberPagination

class CategoryDetailAPI(RetrieveUpdateDestroyAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    lookup_field = 'id'

class ProductListAPI(ListCreateAPIView):
    queryset = models.Product.objects.prefetch_related('category', 'tags').all()
    serializer_class = serializers.ProductSerializer
    pagination_class = PageNumberPagination
    
    def create(self, request, *args, **kwargs):
        serializer = serializers.ValidateProduct(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': serializer.errors})
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')
        category_id = serializer.validated_data.get('category_id')
        tags = serializer.validated_data.get('tags')
        
        product = models.Product.objects.create(title=title, description=description, price=price, category_id=category_id)
        product.tags.set(tags)
        product.save()
        return Response(status=status.HTTP_201_CREATED, data={'id': product.id})


class ProductDetailAPI(RetrieveUpdateDestroyAPIView):
    queryset = models.Product.objects.prefetch_related('category', 'tags').all()
    serializer_class = serializers.ProductSerializer
    lookup_field = 'id'
    
    def update(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = serializers.ValidateProduct(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        product.title = serializer.validated_data.get('title')
        product.description = serializer.validated_data.get('description')
        product.price = serializer.validated_data.get('price')
        product.category_id = serializer.validated_data.get('category_id')
        product.tags.set(serializer.validated_data.get('tags'))
        product.save()
        return Response({'status': 'done!'})

class ReviewListAPI(ListCreateAPIView):
    queryset = models.Review.objects.prefetch_related('product').all()
    serializer_class = serializers.ReviewSerializer
    pagination_class = PageNumberPagination
    
    def create(self, request, *args, **kwargs):
        serializer = serializers.ValidateReview(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': serializer.errors})
        text = serializer.validated_data.get('text')
        stars = serializer.validated_data.get('stars')
        product_id = serializer.validated_data.get('product_id')

        review = models.Review.objects.create(text=text, stars=stars, product_id=product_id)
        return Response(status=status.HTTP_201_CREATED, data={'status': 'done!'})

class ReviewDetailAPI(RetrieveUpdateDestroyAPIView):
    queryset = models.Review.objects.prefetch_related('product').all()
    serializer_class = serializers.ReviewSerializer
    lookup_field = 'id'
    
    def update(self, request, *args, **kwargs):
        review = self.get_object()
        serializer = serializers.ValidateReview(review, data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': serializer.errors})
        review.text = serializer.validated_data.get('text')
        review.stars = serializer.validated_data.get('stars')
        review.product_id = serializer.validated_data.get('product_id')
        review.save()
        return Response(status=status.HTTP_201_CREATED, data={'status': 'done!'})

class ProductReviewListAPI(ListAPIView):
    queryset = models.Product.objects.prefetch_related('category', 'reviews').all()
    serializer_class = serializers.ProductWithReviewsSerializer
    pagination_class = PageNumberPagination


