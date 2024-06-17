from django.urls import path
from .views import (
    PostList, PostDetail, PostSearch, CreatePost, PostUpdate, PostDelete, IndexView,
upgrade_me, BaseRegisterView, subscriber, unsubscriber, IndexView2
)
from django.contrib.auth.views import LoginView
from django.views.decorators.cache import cache_page


urlpatterns = [

    path('', cache_page(60)(PostList.as_view()), name='general'),
    path('news/<int:pk>', PostDetail.as_view(), name='news_detail'),
    path('articles/<int:pk>', PostDetail.as_view(), name='articles_detail'),
    path('search/', PostSearch.as_view(), name='search'),
    path('news/create/', CreatePost.as_view(), name='news_create'),
    path('articles/create/', CreatePost.as_view(), name='articles_create'),
    path('news/<int:pk>/update/', PostUpdate.as_view(), name='news_edit'),
    path('articles/<int:pk>/update/', PostUpdate.as_view(), name='articles_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('signup/', BaseRegisterView.as_view(template_name='registration/signup.html'), name='signup'),
    path('accounts/profile/', IndexView.as_view(), name='profile'),
    path('accounts/profile/sign/upgrade/', upgrade_me, name='upgrade'),
    path('<int:pk>/subscribe/', subscriber, name='subscribe'),
    path('<int:pk>/unsubscribe/', unsubscriber, name='unsubscribe'),
    path('task/', IndexView2.as_view(), name='task'),

]