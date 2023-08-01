from django.urls import path
from django.contrib.auth import views as auth_views

from accounts import views
from .views import home,register,login_user,logout_user
#,search_venues
from flaskapp.views import admin_home_view
 


urlpatterns = [
    path('', home,name="home"),
    path("register", register, name="register"),
    path("login_user", login_user, name="login_user"),
    path("logout_user", logout_user, name="logout_user"),
    #path("register",your_view,name="your_view"),
    #path("search/<int:pk>",views.SearchViewDetail.as_view(),name="search"),
#    path("admin_doctor",views.SearchViewDetail.as_view(),name="search"),
    #2path('',admin,name="adminhome"),
    path('adminhome/', views.admin_home_view, name='adminhome'), # type: ignore
    #path('admin_doctor',search_venues,name='search_venues')
    path("index", views.index, name='index'),
]