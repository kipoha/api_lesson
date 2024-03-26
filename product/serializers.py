from rest_framework import serializers
from product import models
from django.db.models import Count
from rest_framework import exceptions

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = 'id text product stars'.split()

class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(source='products_count', read_only=True)

    class Meta:
        model = models.Category
        fields = 'id name product_count'.split()

class CategoryDetailSerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Category
        fields = 'id name product_count'.split()

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    tags = serializers.SerializerMethodField()
    class Meta:
        model = models.Product
        fields = 'id title description price category tags'.split()
    
    def get_tags(self, product):
        return [i.name for i in product.tags.all()]

class ReviewSerializer2(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        exclude = 'product'.split()

class ProductWithReviewsSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    average_rating = serializers.SerializerMethodField()
    reviews = ReviewSerializer2(many=True)
    class Meta:
        model = models.Product
        fields = 'id title description price category reviews average_rating'.split()
        
    def get_average_rating(self, instance):
        reviews = instance.reviews.all()
        if reviews:
            total_stars = sum(review.stars for review in reviews)
            return total_stars / len(reviews)
        return None

class ValidateCategory(serializers.Serializer):
    name = serializers.CharField(max_length=100)

class ValidateProduct(serializers.Serializer):
    title = serializers.CharField(max_length=100, min_length=3)
    description = serializers.CharField()
    price = serializers.IntegerField()
    category_id = serializers.IntegerField()
    tags = serializers.ListField(child=serializers.IntegerField(min_value=1))
    
    def validate_category_id(self, category_id):
        try:
            models.Product.objects.get(id=category_id)
        except models.Product.DoesNotExist:
            raise exceptions.ValidationError('Category not found!')
        return category_id

    def validate_tags(self, tags):
        tags_list = set(tags)
        tags_db = models.Tag.objects.filter(id__in=tags_list)
        if len(tags_db) != len(tags_list):
            raise exceptions.ValidationError('Tags not found')
        return tags

class ValidateReview(serializers.Serializer):
    text = serializers.CharField()
    stars = serializers.IntegerField(min_value=1, max_value=5)
    product_id = serializers.IntegerField()
