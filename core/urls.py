from django.urls import path
from . import views
from django.conf.urls import handler400, handler500
from .import views

app_name = "core"

urlpatterns = [
    path('home', views.home, name="home"),

    path('', views.signin, name="login"),

    path('signup', views.signup, name="signup"),

    path('logout', views.log_out, name="logout"),

    path('post', views.posting, name="post"),

    path('list', views.list, name="list"),

    path('delete/<int:pk>', views.deletion, name="delete")

]
handler404 = views.error_404
handler500 = views.error_500

