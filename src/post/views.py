from operator import attrgetter

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from .form import CreatePostForm
from .models import PostModel


# index retrieve all data of search data.
def index(request):
    POSTS_PER_PAGE = 5
    context = {}
    # 'query' for search parameters | default is ""
    query = ""
    if request.GET:
        query = request.GET.get('q', '')
        context['query'] = str(query)

    # Query data follow by 'query' variable
    posts = sorted(get_blog_queries(query), key=attrgetter('updated_at'), reverse=True)

    # Paginate declare
    page = request.GET.get('page', POSTS_PER_PAGE)
    # Assign Paginator class with (list data & data per page)
    blog_posts_paginator = Paginator(posts, POSTS_PER_PAGE)

    # Set posts value for each paginated page
    try:
        posts = blog_posts_paginator.page(page)
    except PageNotAnInteger:
        posts = blog_posts_paginator.page(POSTS_PER_PAGE)
    except EmptyPage:
        posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)

    # Assign posts to context dict
    context['posts'] = posts
    # return template and context data
    return render(request, 'index.html', context)


def create(request):
    context = {}
    # Get form field data
    form = CreatePostForm(request.POST or None)
    # Validate form
    if form.is_valid():
        # Save to database
        form.save()
    context['form'] = form
    # return template and context data
    return render(request, 'create.html', context)


def update(request, slug):
    context = {}
    # Get data or fail 404
    obj = get_object_or_404(PostModel, slug=slug)
    # Get form field data
    form = CreatePostForm(request.POST or None, instance=obj)
    # Validate form
    if form.is_valid():
        form.save()
        return redirect('post:index')
    context["form"] = form
    context["slug"] = slug
    # return template and context data
    return render(request, 'update.html', context)


def delete(request, slug):
    obj = get_object_or_404(PostModel, slug=slug)
    if request.method == 'POST':
        obj.delete()
        return redirect('post:index')


# Get data function affect by query
def get_blog_queries(query=None):
    # Create queries list
    queries = []
    # Split spaces foreach condition
    query = query.split(" ")
    # Loop through query
    for q in query:
        # posts is group posts data match query
        posts = PostModel.objects.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q) |
            Q(author__icontains=q)
        ).distinct()
        # append all matching posts to queries
        for post in posts:
            if post not in queries:
                queries.append(post)
    # return a list of set would remove duplicates post
    return list(set(queries))
