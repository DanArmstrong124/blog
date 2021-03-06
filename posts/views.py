from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils import timezone
from .models import Post
from .forms import BlogPostForm
from accounts import views


def get_posts(request):
    """
    Create a view that will return a list
    of Posts that were published prior to 'now'
    and render them to the 'blogposts.html' template
    """
    if request.user.is_authenticated:
        posts = Post.objects.filter(published_date__lte=timezone.now()
            ).order_by('-published_date')
        return render(request, "blogposts.html", {'posts': posts})
    else:
        return(redirect(reverse('registration')))
        


def post_detail(request, pk):
    """
    Create a view that returns a single
    Post object based on the post ID (pk) and
    render it to the 'postdetail.html' template.
    Or return a 404 error if the post is
    not found
    """
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        post.views += 1
        post.save()
        return render(request, "postdetail.html", {'post': post})
    else:
        return(redirect(reverse('registration')))
        


def create_or_edit_post(request, pk=None):
    """
    Create a view that allows us to create
    or edit a post depending if the Post ID
    is null or not
    """
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk) if pk else None
        if request.method == "POST":
            form = BlogPostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                post = form.save()
                return redirect(post_detail, post.pk)
        else:
            form = BlogPostForm(instance=post)
        return render(request, 'blogpostform.html', {'form': form})
    else:
        return(redirect(reverse('registration')))
        