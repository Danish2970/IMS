from django.urls import path
from . import views

urlpatterns = [
    path('', views.location_list, name='location_list'),
    path('add-location/', views.add_location, name='add_location'), # New URL
    path('location/<int:location_id>/', views.floor_list, name='floor_list'),
    path('location/<int:location_id>/add-floor/', views.add_floor, name='add_floor'), # New
    path('floor/<int:floor_id>/', views.room_list, name='room_list'),
    path('floor/<int:floor_id>/add-room/', views.add_room, name='add_room'),
    path('room/<int:room_id>/', views.item_list, name='item_list'),
    path('room/<int:room_id>/add-item/', views.add_item, name='add_item'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('floor/<int:floor_id>/delete/', views.delete_floor, name='delete_floor'),
    path('room/<int:room_id>/delete/', views.delete_room, name='delete_room'),
    path('item/<int:item_id>/delete/', views.delete_item, name='delete_item'),
    path('item/<int:item_id>/edit/', views.edit_item, name='edit_item'),
    path('room/<int:room_id>/export/excel/', views.export_excel, name='export_excel'),
    path('room/<int:room_id>/export/pdf/', views.export_pdf, name='export_pdf'),

    ]