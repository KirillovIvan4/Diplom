from django.urls import path
from . import views

app_name = 'table_reservation'

urlpatterns = [
    path('', views.home, name='home'),
    path('/about_the_restaurant', views.about_the_restaurant, name='about_the_restaurant'),
    path('tables/', views.TableListView.as_view(), name='table_list'),
    path('reserve/', views.ReservationCreateView.as_view(), name='reservation_create'),
    path('my-reservations/', views.ReservationListView.as_view(), name='reservation_list'),
    path('reservation/<int:pk>/edit/', views.ReservationUpdateView.as_view(), name='reservation_update'),
    path('reservation/<int:pk>/delete/', views.ReservationDeleteView.as_view(), name='reservation_delete'),
    path('check-availability/', views.check_availability, name='check_availability'),
    # path('about_the_restaurant', views.about_the_restaurant, name='about_the_restaurant'),
    # path('booking_page', views.booking_page, name='booking_page'),
]