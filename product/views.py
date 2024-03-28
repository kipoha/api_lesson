from rest_framework.decorators import api_view
from rest_framework.response import Response
from product import serializers, models
from rest_framework import status
from django.db.models import Count

@api_view(['GET', 'POST'])
def category_list_view(requets):
    print(requets.user)
    if requets.method == 'GET':
        # categories = models.Category.objects.annotate(product_count=Count('products'))
        categories = models.Category.objects.prefetch_related('products').annotate(products_count=Count('products'))
        data = serializers.CategorySerializer(categories, many=True).data
        return Response(data=data)
    elif requets.method == 'POST':
        serializer = serializers.ValidateCategory(data=requets.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': serializer.errors})
        name = serializer.validated_data.get('name')
        print(name)
        category = models.Category.objects.create(name=name)
        return Response(status=status.HTTP_201_CREATED, data={'id': category.id})

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_view(requets, id):
        try:
            category = models.Category.objects.prefetch_related('products').annotate(product_count=Count('products')).get(id=id)
        except models.Category.DoesNotExist:
            return Response(data={'error': 'not found'}, status=status.HTTP_404_NOT_FOUND)
        if requets.method == 'GET':
            data = serializers.CategoryDetailSerializer(category).data
            return Response(data=data)
        elif requets.method == 'PUT':
            serializer = serializers.ValidateCategory(data=requets.data)
            if not serializer.is_valid():
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': serializer.errors})
            category.name = serializer.validated_data.get('name')
            category.save()
            return Response(status=status.HTTP_201_CREATED, data={'status': 'done!'})
        elif requets.method == 'DELETE':
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT, data={'status': 'deleted!'})
            

@api_view(['GET', 'POST'])
def product_list_view(requets):
    if requets.method == 'GET':
        products = models.Product.objects.prefetch_related('category').all()
        data = serializers.ProductSerializer(products, many=True).data
        return Response(data=data)
    elif requets.method == 'POST':
        serializer = serializers.ValidateProduct(data=requets.data)
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

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_view(requets, id):
        try:
            product = models.Product.objects.get(id=id)
        except models.Product.DoesNotExist:
            return Response(data={'error': 'not found'}, status=status.HTTP_404_NOT_FOUND)
        if requets.method == 'GET':
            data = serializers.ProductSerializer(product, many=False).data
            return Response(data=data)
        elif requets.method == 'PUT':
            serializer = serializers.ValidateProduct(data=requets.data)
            if not serializer.is_valid():
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': serializer.errors})
            product.title = serializer.validated_data.get('title')
            product.description = serializer.validated_data.get('description')
            product.price = serializer.validated_data.get('price')
            product.category_id = serializer.validated_data.get('category_id')
            product.tags.set(serializer.validated_data.get('tags'))
            product.save()
            return Response(status=status.HTTP_201_CREATED, data={'status': 'done!'})
        elif requets.method == 'DELETE':
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT, data={'status': 'deleted!'})

@api_view(['GET', 'POST'])
def review_list_view(requets):
    if requets.method == 'GET':
        reviews = models.Review.objects.prefetch_related('product').all()
        data = serializers.ReviewSerializer(reviews, many=True).data
        return Response(data=data)
    elif requets.method == 'POST':
        serializer = serializers.ValidateReview(data=requets.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': serializer.errors})
        text = serializer.validated_data.get('text')
        stars = serializer.validated_data.get('stars')
        product_id = requets.data.get('product_id')

        review = models.Review.objects.create(text=text, stars=stars, product_id=product_id)
        return Response(status=status.HTTP_201_CREATED, data={'status': 'done!'})

@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_view(requets, id):
        try:
            review = models.Review.objects.get(id=id)
        except models.Review.DoesNotExist:
            return Response(data={'error': 'not found'}, status=status.HTTP_404_NOT_FOUND)
        if requets.method == 'GET':
            data = serializers.ReviewSerializer(review, many=False).data
            return Response(data=data)
        elif requets.method == 'PUT':
            serializer = serializers.ValidateReview(data=requets.data)
            if not serializer.is_valid():
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': serializer.errors})
            review.text = serializer.validated_data.get('text')
            review.stars = serializer.validated_data.get('stars')
            review.product_id = serializer.validated_data.get('product_id')
            review.save()
            return Response(status=status.HTTP_201_CREATED, data={'status': 'done!'})
        elif requets.method == 'DELETE':
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT, data={'status': 'deleted!'})

@api_view(['GET'])
def product_review_view(requets):
    if requets.method == 'GET':
        products = models.Product.objects.prefetch_related('category', 'reviews').all()
        data = serializers.ProductWithReviewsSerializer(products, many=True).data
        return Response(data=data)

