from rest_framework import serializers
from product import models
from django.db.models import Count

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = 'id text product stars'.split()

class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField()
    class Meta:
        model = models.Category
        fields = 'id name product_count'.split()

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(products_count=Count('product'))
        return queryset


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    class Meta:
        model = models.Product
        fields = 'id title description price category'.split()


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
