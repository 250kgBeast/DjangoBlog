from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Post, Author
from .forms import CommentForm, PostAdminForm
from marketing.models import Signup
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


def search(request):
    query_set = Post.objects.all()
    query = request.GET.get('search', '')
    if query:
        query_set = query_set.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query) |
            Q(category__title__icontains=query)
        ).distinct()
    context = {
        'query_set': query_set
    }
    return render(request, 'search_results.html', context)


def get_category_count():
    query_set = Post \
        .objects \
        .values('category__title') \
        .annotate(Count('category__title'))
    return query_set


def index(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]

    if request.method == 'POST':
        email = request.POST['email']
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    context = {
        'object_list': featured,
        'latest': latest
    }
    return render(request, 'index.html', context)


def blog(request):
    post_list = Post.objects.all()
    most_recent = Post.objects.order_by('-timestamp')[0:3]
    category_count = get_category_count()

    paginator = Paginator(post_list, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset': paginated_queryset,
        'page_request_var': page_request_var,
        'most_recent': most_recent,
        'category_count': category_count
    }
    return render(request, 'blog.html', context)


def post(request, id):
    most_recent = Post.objects.order_by('-timestamp')[0:3]
    category_count = get_category_count()
    post = get_object_or_404(Post, id=id)
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        form.instance.user = request.user
        form.instance.post = post
        form.save()
        return redirect(reverse('post-detail', kwargs={
            'id': post.id
        }))
    context = {
        'post': post,
        'most_recent': most_recent,
        'category_count': category_count,
        'form': form
    }
    return render(request, 'post.html', context)


def post_create(request):
    title = 'Create'
    form = PostAdminForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse('post-detail', kwargs={
                'id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, 'post_create.html', context)


def post_update(request, id):
    title = 'Update'
    post = get_object_or_404(Post, id=id)
    form = PostAdminForm(request.POST or None, request.FILES or None, instance=post)
    author = get_author(request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse('post-detail', kwargs={
                'id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, 'post_create.html', context)


def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse('post-list'))
