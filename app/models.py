from django.core.cache import cache
from django.db import models
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import UserCreationForm
from django import forms

from app.tasks import send_message_of_signup


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        send_message_of_signup(request.POST['username'], request.POST['email'])
        return user


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post = Post.objects.filter(author_id = self.user.pk).values('rating')
        comm = Comment.objects.filter(user_id = self.user.pk).values('rating')
        value = Post.objects.filter(author_id = self.user.pk).values('pk')
        sum_post = 0
        sum_comm = 0
        sum_commtopost = 0

        for i in post:
            for j in i.values():
                sum_post += j

        for k in comm:
            for q in k.values():
                sum_comm += q

        for l in value:
            for m in l.values():
                g = Comment.objects.filter(post_id = m).values('rating')
                for f in g:
                    for s in f.values():
                        sum_commtopost += s

        self.rating = sum_post*3 + sum_comm + sum_commtopost
        self.save()

    def __str__(self):
        return f'{self.user}'

class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through='Subscribe', related_name='posts')

    def __str__(self):
        return f'{self.title}'

class Subscribe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Post(models.Model):
    objects = None
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    it_news = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory', related_name='categories')
    title = models.CharField(max_length = 50)
    text = models.TextField()
    rating = models.IntegerField(default=0)


    def like(self):
        self.rating += 1 if self.rating <= 100 else 100
        self.save()

    def dislike(self):
        self.rating -= 1 if self.rating >= 0 else 0
        self.save()

    def preview(self):
        _ = '...'
        return self.text[:124] + _ if len(self.text) >= 124 else self.text[:124]

    def __str__(self):
        return f'{self.title} : {self.text} : {self.author}'

    def get_absolute_url(self):
        if self.it_news == True:
            return f'/news/{self.id}'
        else:
            return f'/articles/{self.id}'

    def save(self, *args, **kwargs):
        flag = 'news' if self.it_news == True else 'articles'
        super().save(*args, **kwargs)
        cache.delete(f'{flag}-{self.pk}')
class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1 if self.rating < 100 else 100
        self.save()
    def dislike(self):
        self.rating -= 1 if self.rating > 0 else 0
        self.save()

    def __str__(self):
        return f'{self.text} : {self.user}'

class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )

