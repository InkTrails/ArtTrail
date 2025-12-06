from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('compare/', views.compare, name='compare'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('upload/', views.UploadView.as_view(), name='upload'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/delete/', views.DeletePostView.as_view(), name='delete_post'),
    path('bulk_delete/', views.bulk_delete, name='bulk_delete'),
]