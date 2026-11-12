from django.urls import path
from common import views

app_name = 'common'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('like/<int:photo_pk>/', views.like_functionality_view, name='like'),
    path('comment/<int:photo_pk>/', views.add_comment_view, name='comment'),
    path('share/<int:photo_pk>/', views.share_functionality, name='share'),

]