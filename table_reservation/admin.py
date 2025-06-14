from django.contrib import admin

from table_reservation.models import Table, Reservation


@admin.register(Table)
class Table(admin.ModelAdmin):
    list_display = ('pk', 'number','capacity', 'is_active',)
    list_filter = ('number',)
    search_fields = ('number',)

@admin.register(Reservation)
class Reservation(admin.ModelAdmin):
    list_display = ('pk', 'user', 'time',)
    list_filter = ('user',)
    search_fields = ('user',)