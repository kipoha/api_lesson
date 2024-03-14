from rest_framework import serializers
from product import models

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = 'id name'.split()

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = 'id title description price category'.split()

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = 'id text product'.split()
