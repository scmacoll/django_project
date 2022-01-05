from django.shortcuts import get_object_or_404, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ( ListView, DetailView, CreateView, UpdateView, DeleteView, )
from .models import Post  


def home(request):
  context = {
    'posts': Post.objects.all()
  }
  return render(request, 'blog/home.html', context)


class PostListView(ListView):
  model = Post
  template_name = 'blog/home.html'
  context_object_name = 'posts'
  ordering = ['-date_posted']
  paginate_by = 5

class UserPostListView(ListView):
  model = Post
  template_name = 'blog/user_posts.html'
  context_object_name = 'posts'
  paginate_by = 5

  def get_queryset(self): # (get object model User, get username that is from url) otherwise 404 error
    user = get_object_or_404(User, username=self.kwargs.get('username'))
    return Post.objects.filter(author=user).order_by('-date_posted') # return the username with user filter



class PostDetailView(DetailView): # has posts details
  model = Post  # <app>/<model>_<viewtype>.html   ==   blog/post_detail.html


class PostCreateView(LoginRequiredMixin, CreateView): # (requires login), only user can update their post, creates posts
  model = Post
  fields = ['title', 'content']

  def form_valid(self, form): # enables blog post created by user
    form.instance.author = self.request.user
    return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): # (requires login), creates posts
  model = Post
  fields = ['title', 'content']

  def form_valid(self, form): # enables blog post created by user
    form.instance.author = self.request.user
    return super().form_valid(form)

  def test_func(self): # UserPassesTestMixin - see if user updating post is the user of the post
    post = self.get_object() # select post that we are trying to update. - "get post"
    if self.request.user == post.author: # if user requesting this function(post), is the author
      return True
    return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView): # require user to be logged in, user must be author to delete, enables deleting of blog posts
  model = Post  # <app>/<model>_<viewtype>.html   ==   blog/post_detail.html
  success_url = '/'

  def test_func(self): # UserPassesTestMixin - see if user updating post is the user of the post
    post = self.get_object() # select post that we are trying to update. - "get post"
    if self.request.user == post.author: # if user requesting this function(post), is the author
      return True
    return False


def about(request):
  return render(request, 'blog/about.html', {'title': 'About'} )