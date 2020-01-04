from django.urls import path

from .views import Category, FavoriteThing

app_name = 'api'

catgories = Category.CategoryView.as_view({
    'get': 'list',
    'post': 'create'
})

one_category = Category.CategoryView.as_view({
    'get': 'retrieve'
})

favorite_things = FavoriteThing.FavoriteThingView.as_view({
    'get': 'list',
    'post': 'create'
})

one_favorite_thing = FavoriteThing.FavoriteThingView.as_view({
    'get': 'retrieve',
    'put': 'update'
})

urlpatterns = [
    path('categories', catgories, name="categories"),
    path('categories/<int:pk>', one_category, name="one_category"),
    path('favorites', favorite_things, name="favorite_things"),
    path('favorites/<int:pk>', one_favorite_thing, name="one_favorite_thing")
]
