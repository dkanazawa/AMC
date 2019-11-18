from django.urls import path
from . import views

app_name = 'event'

urlpatterns = [
    path('', views.EventNew.as_view(), name='event_new'),
    path('new/', views.EventNew.as_view(), name='event_new'),
    path('detail/<uuid:pk>/', views.EventDetail.as_view(), name='event_detail'),
    path('detail/<uuid:pk>/result/new/', views.ResultNew.as_view(), name='result_new'),
    path('detail/<uuid:pk>/result/export/', views.result_export, name='result_export'),
    path('detail/<uuid:event_pk>/result/delete/<int:pk>/', views.GameDelete.as_view(), name='game_delete'),
    path('join/<uuid:pk>/new/', views.PlayerNew.as_view(), name='player_new'),
    path('detail/<uuid:event_pk>/player/<int:pk>/', views.PlayerEdit.as_view(), name='player_edit'),
]
