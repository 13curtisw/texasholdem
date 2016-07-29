from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name = 'my_index'),
    url(r'^user/create$', views.create, name = "my_create"),
    url(r'^main$', views.login, name = 'my_main'),
    url(r'^tables/new$',views.addtable,name = "my_newtable"),
    url(r'^tables/new$',views.addtable,name = "my_player"),
    url(r'^user/edit/$',views.edit, name = "my_edit"),
    url(r'^user/update/$',views.update, name = "my_update"),
    url(r'^user/profile/(?P<id>\d+)$',views.profile, name = "my_profile"),
    url(r'^tables/',views.join, name = "my_join"),
    url(r'^logout$',views.logout, name = "my_logout"),
    url(r'^leave$',views.leave, name = "my_leave"),
    url(r'^leaderboard$',views.leaderboard, name = "my_leaderboard"),

]
