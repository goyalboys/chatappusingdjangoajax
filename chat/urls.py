from django.urls import path
from . import views
urlpatterns = [
    #path('',views.home,name='home'),
    path('login/',views.login,name='login'),#both are valid
    path('signup/',views.signup,name='signup'),
    path('logout/',views.signout),
path('',views.home,name='home'),
    path("<pk>/", views.chatroom, name="chatroom"),
    path("ajax/<int:pk>/", views.ajax_load_messages, name="chatroom-ajax"),
]
