from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Post, Category
from .serializers import PostSerializer, CategorySerializer


# GET ALL POSTS + CREATE POST
@api_view(['GET', 'POST'])
def post_list_create(request):

    if request.method == 'GET':
        posts = Post.objects.all().order_by('-id')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        title = request.data.get('title')
        content = request.data.get('content')
        category_name = request.data.get('category')

        category, _ = Category.objects.get_or_create(name=category_name)

        post = Post.objects.create(
            title=title,
            content=content,
            category=category,
            author=request.user if request.user.is_authenticated else None
        )

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# GET, UPDATE, DELETE SINGLE POST
@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, pk):

    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=404)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    if request.method == 'PUT':
        post.title = request.data.get('title', post.title)
        post.content = request.data.get('content', post.content)

        category_name = request.data.get('category')
        if category_name:
            category, _ = Category.objects.get_or_create(name=category_name)
            post.category = category

        post.save()
        return Response(PostSerializer(post).data)

    if request.method == 'DELETE':
        post.delete()
        return Response({"message": "Deleted successfully"})