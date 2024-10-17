from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post

# Create your views here.

# ListView for displaying all blog posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'

# DetailView for displaying a single blog post
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

# CreateView for adding a new blog post
class PostCreateView(CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('post_list')

# UpdateView for editing a blog post
class PostUpdateView(UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('post_list')

# DeleteView for deleting a blog post
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment

@login_required  # Ensure only authenticated users can add comments
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)  # Fetch the post being commented on

    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        
        # Automatically associate the logged-in user with the comment
        Comment.objects.create(post=post, user=request.user, comment=comment_text)
        
        # Redirect back to the post detail page (or another page)
        return redirect('post_detail', post_id=post.id)

    return render(request, 'add_comment.html', {'post': post})
