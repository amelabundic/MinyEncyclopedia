from django.urls import path # type: ignore

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:title>/', views.entry_page, name='entry_page'),
    path('search/', views.search, name='search'),
    path('create/', views.create_page, name='create_page'),
    path('edit/<str:title>/', views.edit_page, name='edit_page'),
    path('random/', views.random_page, name='random_page'),
]
