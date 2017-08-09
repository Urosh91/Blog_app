from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from comments.forms import CommentForm
from comments.models import Comment
from .models import Post
from .forms import PostForm
from . utils import read_time


@login_required
def post_create(request):
    # if not (request.user.is_staff or request.user.is_superuser):
    #     raise Http404

    # if not request.user.is_authenticated:
    #     raise Http404

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        # print(form.cleaned_data.get('title'))
        post.user = request.user
        post.save()
        messages.success(request, 'Successfully Created')
        return HttpResponseRedirect(reverse('posts:detail', kwargs={'slug': post.slug}))
        # return HttpResponseRedirect(post.get_absolute_url())
    if form.errors:
        messages.error(request, 'Invalid Input')
    return render(request, 'posts/post_form.html', {'form': form})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if not post.share_public:
        if not (request.user.is_staff or request.user.is_superuser):
            raise Http404
    initial_data = {
        'content_type': post.get_content_type,
        'object_id': post.id,
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated():
        c_type = form.cleaned_data.get('content_type')
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get('content')
        parent_obj = None
        try:
            parent_id = int(request.POST.get('parent_id'))
        except ValueError:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists():
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
            parent=parent_obj,
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    comments = post.comments()
    return render(request, 'posts/single_post.html',
                  {'post': post, 'comments': comments, 'comment_form': form})


def post_list(request):
    posts_list = Post.objects.all_published()
    if request.user.is_staff or request.user.is_superuser:
        posts_list = Post.objects.all()
    # posts_list = Post.objects.filter(share_public=True)
    query = request.GET.get('q')
    if query:
        posts_list = posts_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()
    title = 'List'
    paginator = Paginator(posts_list, 4)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    return render(request, 'posts/post_list.html', {'posts': posts, 'title': title})


def post_update(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if not (request.user.is_staff or request.user.is_superuser or post.user == request.user):
        response = HttpResponse('You do not have a permission to do that')
        response.status_code = 403
        return response
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
        messages.success(request, 'Successfully Created')
        return HttpResponseRedirect(reverse('posts:detail', kwargs={'slug': post.slug}))
        # return HttpResponseRedirect(post.get_absolute_url())
    if form.errors:
        messages.error(request, 'Invalid Input')
    return render(request, 'posts/post_form.html', {'post': post, 'form': form})


def post_delete(request, slug):
    # if not (request.user.is_staff or request.user.is_superuser):
    #     raise Http404
    post = get_object_or_404(Post, slug=slug)
    if post.user != request.user:
        if not (request.user.is_staff or request.user.is_superuser):
            response = HttpResponse('You do not have a permission to do that')
            response.status_code = 403
            return response
    if request.method == 'POST':
        post.delete()
        messages.success(request, f' { post.title } has been successfully deleted')
        return redirect('posts:list')
    return render(request, 'posts/confirm_delete.html', {'object': post})