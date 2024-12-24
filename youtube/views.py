from django.shortcuts import render
from .models import Channel, CustomUser, Subscription, Video
from .serializers import  ChannelSerializer, CustomUserSerializer, VideoSerializer
from rest_framework import generics
from .permissions import IsOwnerOrReadOnly
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListCreateAPIView,CreateAPIView


from .serializers import RegisterSerializer


class RegisterView(ListCreateAPIView): 
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    
# Token olish (login)
class LoginView(TokenObtainPairView):
    pass

# Tokenni yangilash
class RefreshTokenView(TokenRefreshView):
    pass

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()  # Tokenni qora ro'yxatga qo'shish
            return Response({"message": "Logged out successfully"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class VideoListCreateView(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            subscribed_channels = user.subscriptions.values_list('id', flat=True)
            return Video.objects.filter(channel_id__in=subscribed_channels)
        return Video.objects.all().order_by('?')

class VideoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

class ChannelListCreateView(generics.ListCreateAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ChannelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = [IsOwnerOrReadOnly]

class CustomUserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class CustomUserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class SubscribeView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        channel_id = request.data.get('channel_id')
        channel = Channel.objects.get(id=channel_id)
        Subscription.objects.create(user=request.user, channel=channel)
        return Response({'status': 'subscribed'})

class UnsubscribeView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        channel_id = request.data.get('channel_id')
        Subscription.objects.filter(user=request.user, channel_id=channel_id).delete()
        return Response({'status': 'unsubscribed'})
