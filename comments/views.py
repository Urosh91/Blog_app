from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CommentForm
from .models import Comment


@login_required
def comment_delete(request, pk):
    # obj = get_object_or_404(Comment, pk=pk)
    try:
        obj = Comment.objects.get(pk=pk)
    except:
        raise Http404

    if obj.user != request.user:
        if not (request.user.is_staff or request.user.is_superuser):
            # messages.error(request, 'You do not have a permission to do that')
            # raise Http404
            response = HttpResponse('You do not have a permission to do that')
            response.status_code = 403
            return response
            # return render(request, 'comments/confirm_delete.html', {'object': obj})

    if request.method == 'POST':
        parent_object_url = obj.content_object.get_absolute_url()
        obj.delete()
        messages.success(request, f' { obj.content } has been successfully deleted')
        return HttpResponseRedirect(parent_object_url)
    return render(request, 'comments/confirm_delete.html', {'object': obj})


def comment_thread(request, pk):
    # obj = get_object_or_404(Comment, pk=pk)
    try:
        obj = Comment.objects.get(pk=pk)
    except:
        raise Http404
    if not obj.is_parent:
        obj = obj.parent
    initial_data = {
        'content_type': obj.content_type,
        'object_id': obj.object_id,
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    # print(form.errors)
    # print(dir(form))
    if form.is_valid() and request.user.is_authenticated:
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
    return render(request, 'comments/comment_thread.html', {'comment': obj, 'form': form})