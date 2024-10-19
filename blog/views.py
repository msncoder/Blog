from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Like, Comment
from .forms import PostForm, CommentForm

# View for the landing page showing all posts
def index(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/index.html', {'posts': posts})

# View for post details and handling comments
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'form': form})

# View to handle likes
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()  # If like exists, remove it (toggle feature)

    return redirect('post_detail', post_id=post.id)

# @login_required
# def add_comment(request, post_id):
#     if request.method == "POST":
#         content = request.POST.get('content')
#         post = Post.objects.get(id=post_id)
#         comment = Comment(post=post, user=request.user, content=content)
#         comment.save()
#         return redirect('index')  # Redirect back to the index page

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from django.contrib.auth.decorators import login_required

@login_required
def add_comment(request, post_id):
    if request.method == "POST":
        content = request.POST.get('content')
        post = get_object_or_404(Post, id=post_id)
        comment = Comment(post=post, user=request.user, content=content)
        comment.save()

        # Prepare the response data
        data = {
            'username': request.user.username,
            'content': comment.content,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),  # Format the timestamp if needed
        }
        return JsonResponse(data)
    

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from .models import Post, Like

@require_POST  # Make sure this view only handles POST requests
def like_post(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=post_id)
        liked = False
        # Check if the user has already liked this post
        like = Like.objects.filter(post=post, user=request.user).first()

        if like:
            # If like exists, delete it (unlike)
            like.delete()
        else:
            # If not liked yet, create a new like
            Like.objects.create(post=post, user=request.user)
            liked = True

        # Return JSON response with the like status and updated like count
        return JsonResponse({
            'liked': liked,
            'likes_count': post.likes.count(),
        })
    return JsonResponse({'error': 'User not authenticated'}, status=403)


from django.shortcuts import render, get_object_or_404
from .models import Post

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post_detail.html', {'object_or_url': post.get_absolute_url()})