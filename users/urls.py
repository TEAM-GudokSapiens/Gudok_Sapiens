from django.urls import path
from . import views

app_name='users'

urlpatterns = [
    path('signup/', view=views.signup, name='signup'),
    path('login/', view=views.login, name='login'),   
    path('logout/', view=views.logout, name='logout'),  
    
    path('<int:pk>/detail', view=views.detail, name='detail'),
    path('change_pw/', view=views.change_pw, name='change_pw'),
]