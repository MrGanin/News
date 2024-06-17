from django import forms
from django.shortcuts import render
from .models import Post, Category


class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = ['title', 'category', 'text']

