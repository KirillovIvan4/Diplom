import secrets

from django.contrib.auth.views import PasswordResetView
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, ListView
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from config.settings import EMAIL_HOST_USER
from .forms import CustomUserCreationForm, PasswordRecoveryForm
from .models import User
import logging



def personal_account(request):
    return render(request, 'users/personal_account.html')

class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('table_reservation:home')

    def form_valid(self, form):
        user = form.save()
        user.is_active = True
    #     token = secrets.token_hex(16)
    #     host = self.request.get_host()
    #     user.token = token
    #     user.save()
    #     url = f'http://{host}/users/email-confirm/{token}'
    #     send_mail(
    #         subject='Подтверждение почты',
    #         message=f"Перейдите по ссылке для подтверждения почты {url}",
    #         from_email=EMAIL_HOST_USER,
    #         recipient_list=[user.email],
    #     )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))

class PasswordRecoveryView(TemplateView,PasswordResetView):
    model = User
    template_name = 'users/password_recovery.html'
    form_class = PasswordRecoveryForm
    success_url = reverse_lazy('users:login')



    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        user = User.objects.get(email=email)
        code = secrets.token_hex(8)
        user.set_password(code)
        user.save()

        host = self.request.get_host()
        url = f'http://{host}/users/login/'

        send_mail(
            'Восстановление пароля',
            f'Ваш новый пароль {code}, перейдите по ссылке {url}',
            EMAIL_HOST_USER,
            [user.email],
        )
        return HttpResponseRedirect('/users/login/')

@permission_required("users.view_user")
def block_user(self, pk):
    user = User.objects.get(pk=pk)
    user.is_active = {user.is_active: False, not user.is_active: True}[True]
    user.save()
    return redirect(reverse("users:user_list"))

class UserListView(ListView):
    model = User
    context_object_name = 'User'

    def dispatch(self, request, *args, **kwargs):
        if not (self.request.user.is_superuser or self.request.user.groups.filter(name="Менеджеры").exists()):
            raise PermissionDenied("У вас нет прав для редактирования публикации.")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """
        Исключаем суперпользователей и пользователей из группы "Менеджеры".
        """
        # Получаем всех пользователей, кроме суперпользователей
        queryset = User.objects.filter(is_superuser=False)

        # Исключаем пользователей из группы "Менеджеры"
        manager_group = Group.objects.get(name="Менеджеры")
        queryset = queryset.exclude(groups=manager_group)

        return queryset