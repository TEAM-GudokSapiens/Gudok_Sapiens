from django.urls import path
from . import views
from users.views import AccountUpdateView

app_name = "users"

urlpatterns = [
    path('signup/', views.Signup.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('update/<int:pk>', AccountUpdateView.as_view(), name='update'),
    path('delete/', views.profile_delete_view, name='delete'),
    path('update/password', views.update_password, name='update_password'),
    path('dibs_list/', views.dibs_list, name='dibs_list'),
    path('reviews_list/', views.reviews_list, name='reviews_list'),
    path('registerauth/', views.register_success, name='register_success'),
    path('activate/<str:uid64>/<str:token>/', views.activate, name='activate'),
    path('agreement/', views.AgreementView.as_view(), name='agreement'),
    path('recovery/id/', views.RecoveryIdView.as_view(), name='recovery_id'),
    path('recovery/id/find/', views.ajax_find_id_view, name='ajax_id'),

]
