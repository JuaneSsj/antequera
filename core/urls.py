from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('clients/', views.ClientListView.as_view(), name='client_list'),
    path('clients/archive/', views.ClientArchiveListView.as_view(), name='client_archive_list'),
    path('clients/<int:pk>/archive-toggle/', views.client_archive_toggle, name='client_archive_toggle'),
    path('clients/new/', views.ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/', views.ClientDetailView.as_view(), name='client_detail'),
    path('clients/<int:pk>/edit/', views.ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/delete/', views.ClientDeleteView.as_view(), name='client_delete'),
    path('clients/<int:client_id>/measurements/new/', views.MeasurementCreateView.as_view(), name='measurement_create'),
    path('clients/<int:client_id>/images/new/', views.ClientImageCreateView.as_view(), name='image_create'),
    path('trainer/', views.TrainerDetailView.as_view(), name='trainer_detail'),
    path('trainer/new/', views.TrainerCreateView.as_view(), name='trainer_create'),
    path('trainer/edit/', views.TrainerUpdateView.as_view(), name='trainer_update'),
    path('trainer/delete/', views.TrainerDeleteView.as_view(), name='trainer_delete'),
    path('business/edit/', views.BusinessProfileUpdateView.as_view(), name='business_profile_update'),
    path('agenda/trainer/', views.TrainerAgendaView.as_view(), name='trainer_agenda'),
    path('agenda/client/', views.ClientBookingView.as_view(), name='client_booking'),
]
