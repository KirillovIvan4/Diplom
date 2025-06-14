from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Table(models.Model):
    TABLE_SHAPES = [
        ('round', 'Круглый'),
        ('square', 'Квадратный'),
        ('rectangular', 'Прямоугольный'),
    ]

    number = models.PositiveIntegerField(unique=True, verbose_name='Номер столика')
    capacity = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name='Вместимость'
    )
    shape = models.CharField(max_length=20, choices=TABLE_SHAPES, verbose_name='Форма')
    description = models.TextField(blank=True, verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Доступен для бронирования')

    class Meta:
        verbose_name = 'Столик'
        verbose_name_plural = 'Столики'
        ordering = ['number']

    def __str__(self):
        return f'Столик №{self.number} ({self.capacity} персон)'


class Reservation(models.Model):
    TIME_SLOTS = [
        ('10:00', '10:00'), ('11:00', '11:00'), ('12:00', '12:00'),
        ('13:00', '13:00'), ('14:00', '14:00'), ('15:00', '15:00'),
        ('16:00', '16:00'), ('17:00', '17:00'), ('18:00', '18:00'),
        ('19:00', '19:00'), ('20:00', '20:00'), ('21:00', '21:00'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations', verbose_name='Пользователь')
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='reservations', verbose_name='Столик')
    date = models.DateField(verbose_name='Дата бронирования')
    time = models.CharField(max_length=5, choices=TIME_SLOTS, verbose_name='Время бронирования')
    guests = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name='Количество гостей'
    )
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_confirmed = models.BooleanField(default=False, verbose_name='Подтверждено')

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        ordering = ['-date', 'time']
        unique_together = ['table', 'date', 'time']

    def __str__(self):
        return f'Бронирование #{self.id} - Столик {self.table.number} на {self.date} {self.time}'