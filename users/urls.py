from django.urls import path
from . import views
from users.views import UpdateView, DeleteView

app_name = 'users'

urlpatterns = [
    path('signup/', view=views.signup, name='signup'),
    path('login/', view=views.login, name='login'),
    path('logout/', view=views.logout, name='logout'),
    path('<int:pk>/detail', UpdateView.as_view(), name='detail'),
    path('<int:pk>/delete', DeleteView.as_view(), name='delete'),
]
