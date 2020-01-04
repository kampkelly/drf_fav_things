from functools import wraps

from rest_framework import status
from rest_framework.response import Response
from django.db.models import F

from api.models import FavoriteThing, Category


class ReorderFavoriteThings:
    def check_existing_favorite_thing(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    pass
                    existing_favorite_thing = FavoriteThing.objects.filter(
                        title=args[1].data['title'],
                        category=args[1].data['category']
                    ).first()
                except:
                    return Response({'error': 'Somethings went wrong. Please try again!'}, status=status.HTTP_400_BAD_REQUEST)
                if existing_favorite_thing:
                    return Response({'error': '%s has already been added' % args[1].data['title']}, status=status.HTTP_400_BAD_REQUEST)
                return func(*args, **kwargs)
            return wrapper

    def check_last_favorite_thing_in_category(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                category_exists = Category.objects.filter(
                    id=args[1].data['category']
                ).first()
                
                if not category_exists:
                    return Response({'error': 'Category does not exist'}, status=status.HTTP_404_NOT_FOUND)
                last_favorite_thing_in_category = FavoriteThing.objects.filter(
                    category=args[1].data['category']
                ).order_by('-created_at').first()

                if not last_favorite_thing_in_category:
                    args[1].data['ranking'] = 1

                if ('pk' in kwargs and last_favorite_thing_in_category
                    and args[1].data['ranking'] > last_favorite_thing_in_category.ranking): # noqa
                    args[1].data['ranking'] = last_favorite_thing_in_category.ranking

                if ('pk' not in kwargs and last_favorite_thing_in_category
                    and args[1].data['ranking'] > last_favorite_thing_in_category.ranking): # noqa
                    args[1].data['ranking'] = last_favorite_thing_in_category.ranking + 1 # noqa
            except:
                return Response({'error': 'Something went wrong. Please try again!'}, status=status.HTTP_400_BAD_REQUEST)
            return func(*args, **kwargs)
        return wrapper

    def reorder_favorite_things_on_create(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                FavoriteThing.objects.filter(
                    category=args[1].data['category'],
                    ranking__gte=args[1].data['ranking']
                ).update(ranking=F('ranking') + 1)
            except:
                return Response({'error': 'Something went wrong. Please try again!'}, status=status.HTTP_400_BAD_REQUEST)
            return func(*args, **kwargs)
        return wrapper

    def reorder_favorite_things_on_update(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'pk' in kwargs:
                favorite_thing = kwargs['favorite_thing']
                try:
                    if favorite_thing.ranking < args[1].data['ranking']:
                        FavoriteThing.objects.filter(
                            category=kwargs['category_id'],
                            ranking__gt=favorite_thing.ranking,
                            ranking__lte=args[1].data['ranking']
                        ).exclude(
                            id=kwargs['pk']
                        ).update(ranking=F('ranking') - 1)

                    elif favorite_thing.ranking > args[1].data['ranking']:
                        FavoriteThing.objects.filter(
                            category_id=kwargs['category_id'],
                            ranking__lt=favorite_thing.ranking,
                            ranking__gte=args[1].data['ranking']
                        ).exclude(
                            id=kwargs['pk']
                        ).update(ranking=F('ranking') + 1)

                except:
                    return Response({'error': 'Internal Server Error!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return func(*args, **kwargs)
        return wrapper

    def check_if_favorite_thing_exists(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                favorite_thing = FavoriteThing.objects.filter(
                    id=kwargs['pk'],
                    category=args[1].data['category']).first()
            except:
                return Response({'error': 'Something went wrong. Please try again!'}, status=status.HTTP_400_BAD_REQUEST)

            if not favorite_thing:
                return Response({'error': 'Favorite thing does not exist'}, status=status.HTTP_404_NOT_FOUND)
            kwargs['category_id'] = favorite_thing.category_id
            kwargs['favorite_thing'] = favorite_thing

            return func(*args, **kwargs)
        return wrapper
