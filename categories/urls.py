from django.urls import path
from .views import (
    CategoryCreateView,
    CategoryListView,
    CategoryDeleteView,
    CategoryUpdateView,
)


urlpatterns = [
    path('create/', CategoryCreateView.as_view(), name='category-create'),
    path('all_create/', CategoryListView.as_view(), name='all-create'),
    path('category/<int:pk>/delete', CategoryDeleteView.as_view(), name='category-delete'),
    path('category/<int:pk>/update', CategoryUpdateView.as_view(), name='category-update'),
]