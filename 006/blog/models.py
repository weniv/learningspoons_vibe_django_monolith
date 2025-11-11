# blog/models.py
from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="태그명")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="슬러그")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")

    class Meta:
        ordering = ["name"]
        verbose_name = "태그"
        verbose_name_plural = "태그 목록"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("blog:post_by_tag", kwargs={"slug": self.slug})


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="작성자",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")
    is_published = models.BooleanField(default=True, verbose_name="공개 여부")
    view_count = models.IntegerField(default=0, verbose_name="조회수")
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="liked_posts",
        blank=True,
        verbose_name="좋아요",
    )
    thumbnail = models.ImageField(
        upload_to="post_images/", blank=True, null=True, verbose_name="썸네일 이미지"
    )
    tags = models.ManyToManyField(
        Tag, related_name="posts", blank=True, verbose_name="태그"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "게시글"
        verbose_name_plural = "게시글 목록"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("blog:post_detail", kwargs={"pk": self.pk})

    def increment_view_count(self):
        """조회수 1 증가"""
        self.view_count += 1
        self.save(update_fields=["view_count"])

    def total_likes(self):
        """총 좋아요 수 반환"""
        return self.likes.count()


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments", verbose_name="게시글"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="작성자",
    )
    content = models.TextField(verbose_name="댓글 내용")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")

    class Meta:
        ordering = ["created_at"]
        verbose_name = "댓글"
        verbose_name_plural = "댓글 목록"

    def __str__(self):
        return f"{self.author.get_display_name()}: {self.content[:20]}"

    def get_absolute_url(self):
        return self.post.get_absolute_url()
