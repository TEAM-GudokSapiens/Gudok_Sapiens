from django.urls import path
from . import views
from users.views import UpdateView, DeleteView

app_name = 'users'

urlpatterns = [
    path('signup/', view=views.signup, name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('<int:pk>/detail', UpdateView.as_view(), name='detail'),
    path('<int:pk>/delete', DeleteView.as_view(), name='delete'),
]
