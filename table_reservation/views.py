
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
from .models import Reservation, Table
from .forms import ReservationForm
import datetime


def home(request):
    return render(request, 'table_reservation/home.html')

def about_the_restaurant(request):
    return render(request, 'table_reservation/about_the_restaurant.html')


class TableListView(ListView):
    model = Table
    template_name = 'table_reservation/table_list.html'
    context_object_name = 'tables'


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'table_reservation/reservation_form.html'
    success_url = reverse_lazy('reservation_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Столик успешно забронирован!')
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'table_reservation/reservation_list.html'
    context_object_name = 'reservations'

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user).order_by('-date', 'time')


class ReservationUpdateView(LoginRequiredMixin, UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'table_reservation/reservation_form.html'
    success_url = reverse_lazy('reservation_list')

    def form_valid(self, form):
        messages.success(self.request, 'Бронирование успешно обновлено!')
        return super().form_valid(form)

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)


class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    model = Reservation
    template_name = 'table_reservation/reservation_confirm_delete.html'
    success_url = reverse_lazy('reservation_list')

    def form_valid(self, form):
        messages.success(self.request, 'Бронирование успешно отменено!')
        return super().form_valid(form)

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)


def check_availability(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')

        if date and time:
            reserved_tables = Reservation.objects.filter(date=date, time=time).values_list('table_id', flat=True)
            available_tables = Table.objects.filter(is_active=True).exclude(id__in=reserved_tables)

            context = {
                'date': date,
                'time': time,
                'available_tables': available_tables,
            }
            return render(request, 'table_reservation/availability_result.html', context)

    today = timezone.localdate().isoformat()
    max_date = (timezone.localdate() + datetime.timedelta(days=90)).isoformat()

    return render(request, 'table_reservation/check_availability.html', {
        'min_date': today,
        'max_date': max_date,
    })
