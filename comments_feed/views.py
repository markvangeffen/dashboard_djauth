from datetime import datetime
from django.views.generic import TemplateView
from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count
from .forms import PostForm
from .models import Post, Report
from django.contrib.auth import get_user_model

def Comment_Feed(request):
  if request.method == 'POST':
    form = PostForm(request.POST)
    if form.is_valid():
      post = form.save(commit=False)
      post.user = request.user 
      post.save()
      return redirect('comments_feed')
  else:
    form = PostForm()
    posts = Post.objects.filter(hidden=False).order_by('-date_posted').all()

    context = {'form' : form, 'posts' : posts}

  return render(request, 'comments_feed/comments_feed.html', context)

def Delete_Post(request, post_id):
  # check if post belongs to user
  post = Post.objects.get(id=post_id)
  if post.user == request.user:
      post.delete()
  # remove it from the database
  # redirect back to same page
  return redirect('comments_feed')

def Report_Post(request, post_id):
  post = Post.objects.get(id=post_id)

  report, created = Report.objects.get_or_create(reported_by=request.user, post=post)

  if created:
      report.save()

  return redirect('comments_feed')
  
@permission_required('comments_feed.view_report', raise_exception=True)
def Gerapporteerde_Comments(request):
  reports = Post.objects.annotate(times_reported=Count('report')).filter(times_reported__gt=0).all().order_by('-date_posted').all()

  context = {'reports' : reports}

  return render(request, 'comments_feed/gerapporteerde_comments.html', context)

@permission_required('comments_feed.change_post', raise_exception=True)
def Hide_Post(request, post_id):
  post = Post.objects.get(id=post_id)
  post.hidden = True
  post.date_hidden = datetime.now()
  post.hidden_by = request.user
  post.save()
  return redirect('gerapporteerde_comments')

@permission_required('auth.change_user', raise_exception=True)
def Block_User(request, user_id):
  User = get_user_model()

  user = User.objects.get(id=user_id)
  for post in user.post_set.all():
      if not post.hidden:
          post.hidden = True
          post.hidden_by = request.user
          post.date_hidden = datetime.now()
          post.save()

  user.is_active = False
  user.save()

  return redirect('gerapporteerde_comments')