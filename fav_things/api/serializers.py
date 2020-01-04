from rest_framework import serializers

from .models import Category, FavoriteThing

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['name']


class FavoriteThingSerializer(serializers.ModelSerializer):

    class Meta:
        model = FavoriteThing
        fields = ['title', 'description', 'object_metadata', 'ranking', 'category' ]


def save_serializer(serializer):
    """returns a particular response for when serializer passed is valid or not"""
    serializer.save()
    data = {
        "status": "success",
        "data": serializer.data
    }
    return data
