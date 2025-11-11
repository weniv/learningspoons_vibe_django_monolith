# main/templatetags/markdown_extras.py
from django import template
import markdown as md
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.codehilite import CodeHiliteExtension

register = template.Library()


@register.filter(name="markdown")
def markdown_format(text):
    """마크다운 텍스트를 HTML로 변환"""
    return md.markdown(
        text,
        extensions=[
            "fenced_code",
            "codehilite",
            "tables",
            "nl2br",
        ],
    )
