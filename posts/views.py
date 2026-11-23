from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Like
from .serializers import PostSerializer, PostCreateUpdateSerializer, CommentSerializer


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']

    def get_permissions(self):
        permission = permissions.AllowAny if self.request.method == 'GET' else permissions.IsAuthenticated
        return [permission()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateUpdateSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PostCreateUpdateSerializer
        return PostSerializer

    def get_queryset(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return Post.objects.filter(author=self.request.user)
        return Post.objects.all()


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_permissions(self):
        permission = permissions.AllowAny if self.request.method == 'GET' else permissions.IsAuthenticated
        return [permission()]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'])

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    _, created = Like.objects.get_or_create(post=post, user=request.user)
    if created:
        return Response({'message': 'Post liked successfully'}, status=status.HTTP_201_CREATED)
    return Response({'error': 'You have already liked this post'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    try:
        Like.objects.get(post=post, user=request.user).delete()
        return Response({'message': 'Post unliked successfully'}, status=status.HTTP_200_OK)
    except Like.DoesNotExist:
        return Response({'error': 'You have not liked this post'}, status=status.HTTP_400_BAD_REQUEST)
