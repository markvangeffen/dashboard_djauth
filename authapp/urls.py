from django.urls import path
from .views import edit, register
# from .views import dashboard
from django.urls import reverse_lazy
from django.contrib.auth.views import (LoginView, LogoutView, PasswordResetDoneView, PasswordResetView,
                                       PasswordResetCompleteView, PasswordResetConfirmView,
                                       PasswordChangeView, PasswordChangeDoneView,
                                       PasswordResetDoneView)
from .views import homepage, register, edit

app_name = 'authapp'

urlpatterns = [
    path('register/', register, name='register'),
    path('edit/', edit, name='edit'),
        # The next line can override the local_settings: LOGIN_REDIRECT_URL = '/'
        # path('', homepage, name='homepage'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), 
        name='login'),
        # The next line can be overridden by local_settings: LOGOUT_REDIRECT_URL = '/'
        # I chose for a custom template for the logoutView:
    path('logout/', LogoutView.as_view(template_name='authapp/logged_out.html'), 
        name='logout'),   
    path('password_change/', PasswordChangeView.as_view(
        template_name='authapp/password_change_form.html'), 
        name='password_change'),
    path('password_change/dond/', PasswordChangeDoneView.as_view(
        template_name='authapp/password_change_done.html'), 
        name='password_change_done'),
    path('password_reset/', PasswordResetView.as_view(
        template_name='authapp/password_reset_form.html',
        email_template_name='authapp/password_reset_email.html',
        success_url=reverse_lazy('authapp:password_reset_done')), 
        name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(
        template_name='authapp/password_reset_done.html'), 
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='authapp/password_reset_confirm.html',
        success_url=reverse_lazy('authapp:login')), 
        name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(
        template_name='authapp/password_reset_complete.html'), 
        name='password_reset_complete'),

]