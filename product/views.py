from rest_framework.decorators import api_view
from rest_framework.response import Response
from product import serializers, models
from rest_framework import status
from django.db.models import Count

@api_view(['GET'])
def category_list_view(requets):
    categories = models.Category.objects.annotate(product_count=Count('products'))
    data = serializers.CategorySerializer(categories, many=True).data
    return Response(data=data)


@api_view(['GET'])
def category_detail_view(requets, id):
    try:
        categories = models.Category.objects.get(id=id)
    except models.Category.DoesNotExist:
        return Response(data={'error': 'not found'}, status=status.HTTP_404_NOT_FOUND)
    data = serializers.CategorySerializer(categories, many=False).data
    return Response(data=data)


@api_view(['GET'])
def product_list_view(requets):
    products = models.Product.objects.prefetch_related('category').all()
    data = serializers.ProductSerializer(products, many=True).data
    return Response(data=data)


@api_view(['GET'])
def product_detail_view(requets, id):
    try:
        products = models.Product.objects.get(id=id)
    except models.Product.DoesNotExist:
        return Response(data={'error': 'not found'}, status=status.HTTP_404_NOT_FOUND)
    data = serializers.ProductSerializer(products, many=False).data
    return Response(data=data)

@api_view(['GET'])
def review_list_view(requets):
    reviews = models.Review.objects.prefetch_related('product').all()
    data = serializers.ReviewSerializer(reviews, many=True).data
    return Response(data=data)


@api_view(['GET'])
def review_detail_view(requets, id):
    try:
        reviews = models.Review.objects.get(id=id)
    except models.Review.DoesNotExist:
        return Response(data={'error': 'not found'}, status=status.HTTP_404_NOT_FOUND)
    data = serializers.ReviewSerializer(reviews, many=False).data
    return Response(data=data)

@api_view(['GET'])
def product_review_view(requets):
    products = models.Product.objects.prefetch_related('category', 'reviews').all()
    data = serializers.ProductWithReviewsSerializer(products, many=True).data
    return Response(data=data)

