from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Post, Comment
from .forms import CommentForm


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) #3 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except Emptypage:
        posts=paginator.page(paginator.num_pages)
    return render(request, 'Blog/post/list.html', {'page': page, 'posts': posts})

def post_detail(request , year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish_year=year, publish_month=month,
                             publish_day=day)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        else:
            comment_form = CommentForm()
    return render(request, 'Blog/post/detail.html', {'post':post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'Blog/post/list.html'