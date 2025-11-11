# main/urls.py 수정 (또는 blog/urls.py 새로 생성)
from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    # 기본 페이지
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.ContactView.as_view(), name="contact"),
]

# blog URL patterns
blog_patterns = [
    path("blog/", views.PostListView.as_view(), name="post_list"),
    path("blog/create/", views.PostCreateView.as_view(), name="post_create"),
    path("blog/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("blog/<int:pk>/update/", views.PostUpdateView.as_view(), name="post_update"),
    path("blog/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
    path("blog/tag/<str:slug>/", views.PostByTagListView.as_view(), name="post_by_tag"),
    path(
        "blog/<int:post_pk>/comment/create/",
        views.CommentCreateView.as_view(),
        name="comment_create",
    ),
    path(
        "blog/comment/<int:pk>/update/",
        views.CommentUpdateView.as_view(),
        name="comment_update",
    ),
    path(
        "blog/comment/<int:pk>/delete/",
        views.CommentDeleteView.as_view(),
        name="comment_delete",
    ),
]

urlpatterns += blog_patterns

# app_name을 'blog'로 사용하고 싶다면:
# app_name = 'blog'로 변경하고 위의 blog_patterns를 urlpatterns에 직접 추가
