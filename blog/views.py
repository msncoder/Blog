from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Post, Like, Comment
from .forms import PostForm, CommentForm, ContactForm
from blog.decorators import login_required_custom


# View for the landing page showing all posts
def index(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/index.html', {'posts': posts})


# View for post details and handling comments
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    form = CommentForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
        return redirect('post_detail', post_id=post.id)

    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'form': form})


# Ajax-based view for adding comments
@require_POST
def add_comment(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'You must be logged in to comment.'}, status=401)

    content = request.POST.get('content')
    post = get_object_or_404(Post, id=post_id)

    # Create and save the comment
    comment = Comment(post=post, user=request.user, content=content)
    comment.save()

    # Prepare the response data
    data = {
        'username': request.user.username,
        'content': comment.content,
        'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
    }

    return JsonResponse(data)

# View to like or unlike a post

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from .models import Post, Like
from .decorators import login_required_custom

@login_required_custom  # Custom login required decorator
@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    liked = False

    # Check if the user has already liked this post
    like, created = Like.objects.get_or_create(post=post, user=request.user)

    if created:
        # If a new like was created, set liked to True
        liked = True
    else:
        # If the like already exists, delete it (unlike)
        like.delete()

    # Return the updated like count
    return JsonResponse({
        'liked': liked,
        'likes_count': post.likes.count(),  # Get the total likes for the post
    })

# Contact view for submitting the contact form
# @login_required_custom
def contact_view(request):
    form = ContactForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('contact_success')

    return render(request, 'blog/contact.html', {'form': form})


# View for successful contact form submission
def contact_success_view(request):
    return render(request, 'blog/contact_success.html')


# Static "About" page view
def about(request):
    return render(request, 'blog/about.html')
