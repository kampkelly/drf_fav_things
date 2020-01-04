from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from api.models import Category
from api.serializers import CategorySerializer, save_serializer


class CategoryView(ViewSet):
    def list(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            try:
                data = save_serializer(serializer)
                return Response(data, status=status.HTTP_201_CREATED)
            except:
                return Response({'error': 'Server Error!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'error': 'not valid'}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            categories = Category.objects.get(pk=pk)
            serializer = CategorySerializer(categories)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({'error': 'id does not exist'}, status=status.HTTP_404_NOT_FOUND)
