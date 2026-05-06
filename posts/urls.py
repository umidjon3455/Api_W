from django.urls import path
from .views import (
    PostListCreateView, PostRetrieveUpdateDestroyView,
    CommentListCreateView, like_post, unlike_post
)

urlpatterns = [
    # Post endpoints
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),  # GET, POST
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='post-detail'),  # GET, PUT, DELETE
    
    # Comment endpoints
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),  # GET, POST
    
    # Like endpoints
    path('posts/<int:post_id>/like/', like_post, name='like-post'),  # POST
    path('posts/<int:post_id>/unlike/', unlike_post, name='unlike-post'),  # DELETE
]
