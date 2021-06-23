from rest_framework import serializers

from ..models import Category


class CategorySerializers(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    slug = serializers.SlugField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
