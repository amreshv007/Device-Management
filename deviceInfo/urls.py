from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name="login"),
    path('signup', views.signup, name="signup"),
    path('logout', views.logout, name="logout"),
    path('deletetakenrows', views.deleteTakenRows, name="deletetakenrows"),
    path('deletegivenrows', views.deleteGivenRows, name="deletegivenrows"),
    path('edit-profile', views.editProfile, name="editProfile"),
    path('editfname', views.editfname, name="editfname"),
    path('editlname', views.editlname, name="editlname"),
    path('editpassword', views.editpassword, name="editpassword"),
    # path('place', views.place, name="place"),
]