from django.urls import path
from .views import ChannelDetailView, ChannelListCreateView, CustomUserDetailView, CustomUserListView, VideoDetailView, VideoListCreateView, SubscribeView, UnsubscribeView, RegisterView, LoginView, RefreshTokenView, LogoutView

urlpatterns = [
    path('api/videos/', VideoListCreateView.as_view(), name='video-list-create'),
    path('api/videos/<int:pk>/', VideoDetailView.as_view(), name='video-detail'),
    path('api/channels/', ChannelListCreateView.as_view(), name='channel-list-create'),
    path('api/channels/<int:pk>/', ChannelDetailView.as_view(), name='channel-detail'),
    path('api/users/', CustomUserListView.as_view(), name='user-list'),
    path('api/users/<int:pk>/', CustomUserDetailView.as_view(), name='user-detail'),
    path('api/subscribe/', SubscribeView.as_view(), name='subscribe'),
    path('api/unsubscribe/', UnsubscribeView.as_view(), name='unsubscribe'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
]