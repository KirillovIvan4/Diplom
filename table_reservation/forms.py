from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Reservation, Table
import datetime



class ContactForm(forms.Form):
    name = forms.CharField(label='Ваше имя', max_length=100)
    email = forms.EmailField(label='Email')
    message = forms.CharField(label='Сообщение', widget=forms.Textarea)


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['table', 'date', 'time', 'guests', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['table'].queryset = Table.objects.filter(is_active=True)

        # Установка минимальной даты (сегодня)
        today = timezone.localdate()
        self.fields['date'].widget.attrs['min'] = today.isoformat()

        # Установка максимальной даты (3 месяца вперед)
        max_date = today + datetime.timedelta(days=90)
        self.fields['date'].widget.attrs['max'] = max_date.isoformat()

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < timezone.localdate():
            raise ValidationError("Нельзя забронировать столик на прошедшую дату.")
        return date

    def clean(self):
        cleaned_data = super().clean()
        table = cleaned_data.get('table')
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        guests = cleaned_data.get('guests')

        if table and date and time:
            # Проверка, что столик не забронирован на это время
            if Reservation.objects.filter(table=table, date=date, time=time).exists():
                raise ValidationError("Этот столик уже забронирован на выбранное время.")

            # Проверка вместимости столика
            if guests and guests > table.capacity:
                raise ValidationError(f"Этот столик вмещает максимум {table.capacity} гостей.")

        return cleaned_data