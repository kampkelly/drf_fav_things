from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from api.models import FavoriteThing
from api.serializers import FavoriteThingSerializer, save_serializer
from api.helpers.reorder_favorite_things import ReorderFavoriteThings


class FavoriteThingView(ViewSet):
    def list(self, request):
        favorite_things = FavoriteThing.objects.all()
        serializer = FavoriteThingSerializer(favorite_things, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
   
    @ReorderFavoriteThings.check_existing_favorite_thing
    @ReorderFavoriteThings.check_last_favorite_thing_in_category
    @ReorderFavoriteThings.reorder_favorite_things_on_create
    def create(self, request):
        serializer = FavoriteThingSerializer(data=request.data)
        if serializer.is_valid():
            try:
                data = save_serializer(serializer)
                return Response(data, status=status.HTTP_201_CREATED)
            except:
                return Response({'error': 'Internal Server Error!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'error': 'not valid'}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            favorite_thing = FavoriteThing.objects.get(pk=pk)
            serializer = FavoriteThingSerializer(favorite_thing)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except FavoriteThing.DoesNotExist:
            return Response({'error': 'id does not exist'}, status=status.HTTP_404_NOT_FOUND)

    @ReorderFavoriteThings.check_if_favorite_thing_exists
    @ReorderFavoriteThings.check_last_favorite_thing_in_category
    @ReorderFavoriteThings.reorder_favorite_things_on_update
    def update(self, request, pk=None, **kwargs):
        try:
            favorite_thing = FavoriteThing.objects.get(pk=pk)
            if favorite_thing:
                serializer = FavoriteThingSerializer(favorite_thing, data=request.data, partial=True)
                if serializer.is_valid():
                    try:
                        data = save_serializer(serializer)
                        return Response(data, status=status.HTTP_200_OK)
                    except:
                        return Response({'error': 'Internal Server Error!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                return Response({'error': 'not valid'}, status=status.HTTP_400_BAD_REQUEST)
        except FavoriteThing.DoesNotExist:
            return Response({'error': 'id does not exist'}, status=status.HTTP_404_NOT_FOUND)
