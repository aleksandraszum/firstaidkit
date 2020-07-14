from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^signup/$', views.signup_view, name="signup"),
    url(r'^display/$', views.display, name='display'),
    url(r'^buy/$', views.buy, name='buy'),
    url(r'^use/$', views.use, name='use'),
    url(r'^utylize/$', views.utylize, name='utylize'),
]

