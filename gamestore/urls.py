"""gamestore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from storeapp import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/player_registration/$', views.register_player),
    url(r'^accounts/developer_registration/$', views.register_dev),
    url(r'^accounts/auth/$', views.auth_view),
    url(r'^home/$', views.home),
    url(r'^accounts/logout/$', views.logout),
    url(r'^accounts/login/$', views.custom_login),
    url(r'^accounts/loggedin/$', views.loggedin),
    url(r'^accounts/invalid/$', views.invalid_login),
    url(r'^accounts/registration_success/$', views.register_success),
    url(r'^accounts/$', views.account_page),
    url(r'^accounts/add/$', views.add_game),
    url(r'^games/$', views.all_games),
    url(r'^games/(\d+)/$', views.gamepage),
    url(r'^activate$', views.activate_account),
    url(r'^buy/(\d+)/$', views.buy_game),
    url(r'^buy_success/$', views.buy_success),
    url(r'^buy_cancel/$', views.buy_cancel),
    url(r'^buy_fail/$', views.buy_fail),
    url(r'^accounts/games/(\d+)/$', views.gamepage_dev),
    url(r'^accounts/games/(\d+)/edit/$', views.update_game),
    url(r'^update_score/$', views.update_highscores),
    url(r'^$', views.home),
    url(r'^accounts/games/(\d+)/deactivate/$', views.de_or_reactivate_game),
    url(r'^accounts/games/(\d+)/reactivate/$', views.de_or_reactivate_game),
    url(r'^load_game/$', views.load_game),
    url(r'^save_game/$', views.save_game),
    url(r'^search/$', views.search_games),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^accounts/social_registration/$', views.social_register),
    url(r'^accounts/change_password/$', views.password_change),
]
