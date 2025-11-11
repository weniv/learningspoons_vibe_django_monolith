# blog/forms.py
from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "tags", "thumbnail", "is_published"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent",
                    "placeholder": "제목을 입력하세요",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent",
                    "rows": 15,
                    "placeholder": "마크다운 형식으로 작성 가능합니다",
                }
            ),
            "tags": forms.CheckboxSelectMultiple(attrs={"class": "mt-1"}),
            "thumbnail": forms.FileInput(
                attrs={
                    "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                }
            ),
            "is_published": forms.CheckboxInput(
                attrs={
                    "class": "w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                }
            ),
        }
        labels = {
            "title": "제목",
            "content": "내용",
            "tags": "태그",
            "thumbnail": "썸네일 이미지",
            "is_published": "공개",
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent",
                    "rows": 3,
                    "placeholder": "댓글을 입력하세요",
                }
            ),
        }
        labels = {
            "content": "댓글",
        }
