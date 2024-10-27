# from django.shortcuts import render, get_object_or_404, redirect
# from django.urls import reverse_lazy

# from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_POST
# from .models import Post, Like, Comment
# from .forms import PostForm, CommentForm, ContactForm
# from blog.decorators import login_required_custom


# # View for the landing page showing all posts
# # def index(request):
# #     posts = Post.objects.all().order_by('-created_at')
    
# #     form = SubscriberForm()

# #     return render(request, 'blog/index.html', {'posts': posts,'form':form})


# def index(request):
#     posts = Post.objects.all().order_by('-created_at')
    
#     # Prepare a set of liked post IDs for the logged-in user
#     liked_post_ids = set()
#     if request.user.is_authenticated:
#         liked_posts = Like.objects.filter(user=request.user).values_list('post_id', flat=True)
#         liked_post_ids = set(liked_posts)

#     form = SubscriberForm()

#     return render(request, 'blog/index.html', {
#         'posts': posts,
#         'form': form,
#         'liked_post_ids': liked_post_ids,  # Pass the liked post IDs to the template
#     })


# # View for post details and handling comments
# def post_detail(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     comments = post.comments.all()
#     liked = post.likes.filter(user=request.user).exists()  # Check if the user liked this post
#     likes_count = post.likes.count()
#     form = CommentForm(request.POST or None)

#     if request.method == 'POST' and form.is_valid():
#         comment = form.save(commit=False)
#         comment.post = post
#         comment.user = request.user
#         comment.save()
#         return redirect('post_detail', post_id=post.id)

#     return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form, 'likes_count': likes_count,
#         'liked': liked,})


# # Ajax-based view for adding comments
# @require_POST
# def add_comment(request, post_id):
#     if not request.user.is_authenticated:
#         return JsonResponse({'error': 'You must be logged in to comment.'}, status=401)

#     content = request.POST.get('content')
#     post = get_object_or_404(Post, id=post_id)

#     # Create and save the comment
#     comment = Comment(post=post, user=request.user, content=content)
#     comment.save()

#     # Prepare the response data
#     data = {
#         'username': request.user.username,
#         'content': comment.content,
#         'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
#     }

#     return JsonResponse(data)

# # View to like or unlike a post

# from django.http import JsonResponse
# from django.shortcuts import get_object_or_404
# from django.views.decorators.http import require_POST
# from .models import Post, Like
# from .decorators import login_required_custom

# @login_required_custom  # Custom login required decorator
# @require_POST
# def like_post(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     liked = False

#     # Check if the user has already liked this post
#     like, created = Like.objects.get_or_create(post=post, user=request.user)

#     if created:
#         # If a new like was created, set liked to True
#         liked = True
#     else:
#         # If the like already exists, delete it (unlike)
#         like.delete()

#     # Return the updated like count
#     return JsonResponse({
#         'liked': liked,
#         'likes_count': post.likes.count(),  # Get the total likes for the post
#     })


# # Contact view for submitting the contact form
# # @login_required_custom
# def contact_view(request):
#     form = ContactForm(request.POST or None)

#     if request.method == 'POST' and form.is_valid():
#         form.save()
#         return redirect('contact_success')

#     else:
#         initial_data = {'name': '', 'email': '','message':''}
#         form = ContactForm(initial=initial_data)
#     return render(request, 'blog/contact.html', {'form': form})

# # View for successful contact form submission
# def contact_success_view(request):
#     return render(request, 'blog/contact_success.html')


# # Static "About" page view
# def about(request):
#     return render(request, 'blog/about.html')






# from django.contrib import messages
# from .models import Subscriber
# from .forms import SubscriberForm

# def subscribe(request):
#     if request.method == 'POST':
#         form = SubscriberForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             if not Subscriber.objects.filter(email=email).exists():
#                 Subscriber.objects.create(email=email)
#                 messages.success(request, "You have successfully subscribed!")
#             else:
#                 messages.warning(request, "This email is already subscribed.")
#             return redirect('index')
#     else:
#         form = SubscriberForm()
#     return render(request, 'blog/index.html', {'form': form})


# # views.py
# from django.shortcuts import render, redirect, get_object_or_404
# from .models import Post, Comment
# from .forms import PostForm, CommentForm
# from django.contrib.auth.decorators import login_required

# @login_required
# def dashboard(request):
#     posts = Post.objects.filter(user=request.user)  # Fetch posts of the logged-in user
#     return render(request, 'blog/dashboard.html', {'posts': posts})


# @login_required
# def create_post(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)  # Handle file uploads
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.user = request.user  # Associate post with the logged-in user
#             post.save()
#             return redirect('dashboard')  # Redirect to the dashboard after creating
#     else:
#         form = PostForm()
#     return render(request, 'blog/create_post.html', {'form': form})

# @login_required
# def update_post(request, post_id):
#     post = get_object_or_404(Post, pk=post_id)
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES, instance=post)
#         if form.is_valid():
#             form.save()
#             return redirect('dashboard')
#     else:
#         form = PostForm(instance=post)
#     return render(request, 'blog/update_post.html', {'form': form, 'post': post})

# @login_required
# def delete_post(request, post_id):
#     post = get_object_or_404(Post, pk=post_id)
#     if request.method == 'POST':
#         post.delete()
#         return redirect('dashboard')
#     return render(request, 'blog/delete_post.html', {'post': post})


# @login_required
# def post_comments(request, post_id):
#     post = get_object_or_404(Post, pk=post_id)
#     comments = post.comments.all()  # Fetch all comments for this post

#     if request.method == 'POST':
#         # Handle adding a new comment
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.user = request.user
#             comment.save()
#             return redirect('post_comments', post_id=post.id)
#     else:
#         form = CommentForm()

#     return render(request, 'blog/post_comments.html', {
#         'post': post,
#         'comments': comments,
#         'form': form,
#     })


# @login_required
# def edit_comment(request, comment_id):
#     comment = get_object_or_404(Comment, pk=comment_id)
#     post = comment.post
    
#     # Ensure the logged-in user is the author of the post
#     if post.user != request.user:
#         return redirect('post_comments', post_id=post.id)

#     if request.method == 'POST':
#         form = CommentForm(request.POST, instance=comment)
#         if form.is_valid():
#             form.save()
#             return redirect('post_comments', post_id=comment.post.id)
#     else:
#         form = CommentForm(instance=comment)

#     return render(request, 'blog/edit_comment.html', {'form': form, 'comment': comment})


# @login_required
# def delete_comment(request, comment_id):
#     comment = get_object_or_404(Comment, pk=comment_id)
#     post = comment.post
    
#     # Ensure the logged-in user is the author of the post
#     if post.user == request.user:
#         comment.delete()

#     return redirect('post_comments', post_id=post.id)


# def search_posts(request):
#     query = request.GET.get('q')
#     if query:
#         results = Post.objects.filter(title__icontains=query) | Post.objects.filter(description__icontains=query)
#     else:
#         results = Post.objects.none()  # Return no results if no query

#     return render(request, 'blog/search_results.html', {'results': results, 'query': query})


from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages

from .models import Post, Like, Comment, Subscriber
from .forms import PostForm, CommentForm, ContactForm, SubscriberForm
from blog.decorators import login_required_custom


# View for the landing page showing all posts
def index(request):
    posts = Post.objects.all().order_by('-created_at')
    
    # Prepare a set of liked post IDs for the logged-in user
    liked_post_ids = set()
    if request.user.is_authenticated:
        liked_posts = Like.objects.filter(user=request.user).values_list('post_id', flat=True)
        liked_post_ids = set(liked_posts)

    form = SubscriberForm()

    return render(request, 'blog/index.html', {
        'posts': posts,
        'form': form,
        'liked_post_ids': liked_post_ids,  # Pass the liked post IDs to the template
    })


# View for post details and handling comments
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    liked = post.likes.filter(user=request.user).exists()  # Check if the user liked this post
    likes_count = post.likes.count()
    form = CommentForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
        return redirect('post_detail', post_id=post.id)

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'likes_count': likes_count,
        'liked': liked,
    })


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
def contact_view(request):
    form = ContactForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('contact_success')

    initial_data = {'name': '', 'email': '', 'message': ''}
    form = ContactForm(initial=initial_data)
    return render(request, 'blog/contact.html', {'form': form})


# View for successful contact form submission
def contact_success_view(request):
    return render(request, 'blog/contact_success.html')


# Static "About" page view
def about(request):
    return render(request, 'blog/about.html')


def subscribe(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if not Subscriber.objects.filter(email=email).exists():
                Subscriber.objects.create(email=email)
                messages.success(request, "You have successfully subscribed!")
            else:
                messages.warning(request, "This email is already subscribed.")
            return redirect('index')
    else:
        form = SubscriberForm()
    return render(request, 'blog/index.html', {'form': form})


@login_required
def dashboard(request):
    posts = Post.objects.filter(user=request.user)  # Fetch posts of the logged-in user
    return render(request, 'blog/dashboard.html', {'posts': posts})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Associate post with the logged-in user
            post.save()
            return redirect('dashboard')  # Redirect to the dashboard after creating
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})


@login_required
def update_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/update_post.html', {'form': form, 'post': post})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('dashboard')
    return render(request, 'blog/delete_post.html', {'post': post})


@login_required
def post_comments(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all()  # Fetch all comments for this post

    if request.method == 'POST':
        # Handle adding a new comment
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_comments', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'blog/post_comments.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    post = comment.post
    
    # Ensure the logged-in user is the author of the post
    if post.user != request.user:
        return redirect('post_comments', post_id=post.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_comments', post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'blog/edit_comment.html', {'form': form, 'comment': comment})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    post = comment.post
    
    # Ensure the logged-in user is the author of the post
    if post.user == request.user:
        comment.delete()

    return redirect('post_comments', post_id=post.id)


def search_posts(request):
    query = request.GET.get('q')
    if query:
        results = Post.objects.filter(title__icontains=query) | Post.objects.filter(description__icontains=query)
    else:
        results = Post.objects.none()  # Return no results if no query

    return render(request, 'blog/search_results.html', {'results': results, 'query': query})
