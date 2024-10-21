from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.db import models


# Post model with title, description, image
class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Add this line

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Check if it's a new post
        if not self.pk:  
            super().save(*args, **kwargs)  # Save the post first
            # Send email to all subscribers
            subscribers = Subscriber.objects.all()
            for subscriber in subscribers:
                send_mail(
                    'New Post: ' + self.title,
                    'Check out our new post: ' + self.title,
                    settings.DEFAULT_FROM_EMAIL,
                    [subscriber.email],
                    fail_silently=False,
                )
        else:
            super().save(*args, **kwargs)

# Like model to track likes on a post by a user


class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')  # Ensure that one user can only like a post once

    def __str__(self):
        return f"{self.user} likes {self.post}"
    


# models.py
from django.db import models

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email






# Comment model to allow multiple comments by a user
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.post}"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name
