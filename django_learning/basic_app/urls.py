from django.conf.urls import url
from . import views


app_name = 'basic_app'

urlpatterns = [
    url(r'^registration/', views.registration, name='register_p'),
    url(r'^user_login/', views.user_login, name='user_login'),
]
