from django.shortcuts import render
from .models import Category, Post,Comment,Profile
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from .forms import PostForm


# Create your views here.
@login_required
def profile(request):
   posts=Post.objects.filter(author=request.user)
   
   profile, created = Profile.objects.get_or_create(user=request.user)

   if request.method=="POST":
      if 'image' in request.FILES:
         profile.image=request.FILES['image']
         profile.save()

   
   return render(request,'profile.html',{'posts':posts,'profile':profile})

@login_required
def home(request):
    posts=Post.objects.all()

#search logic
    query=request.GET.get("q")
    if query:
       posts=posts.filter(Q(title__icontains=query)|Q(category__name__icontains=query))
       

    categories=Category.objects.all()
    users=User.objects.all()


    return render(request,'blog/home.html',{'posts':posts,'categories':categories,'users':users})


@login_required
def create_post(request):

    if request.method == "POST":

        title = request.POST.get("title")
        content = request.POST.get("content")
        image = request.FILES.get("image")
        category_name = request.POST.get("category")

        category, created = Category.objects.get_or_create(
            name=category_name
        )

        Post.objects.create(
            title=title,
            content=content,
            image=image,
            category=category,
            author=request.user
        )

        return redirect('home')

    categories = Category.objects.all()

    return render(
        request,
        'blog/create_post.html',
        {'categories': categories}
    )


@login_required
def edit_post(request,post_id):
   post=get_object_or_404(Post,id=post_id)

   if post.author!= request.user:   #prevents from editing other users posts
         return redirect('home')
   
   if request.method=="POST":
      post.title=request.POST.get("title")
      post.content=request.POST.get("content")

      category_name=request.POST.get("category")

      category,created=Category.objects.get_or_create(name=category_name)


      post.category=category


      if request.FILES.get("image"):
         post.image=request.FILES.get("image")

      post.save()  

      return redirect('home')

   return render(request,'blog/create_post.html',{'edit_mode':True,'post':post}) 
   

#post detail view 
@login_required
def Post_detail(request,id):
    post=get_object_or_404(Post,id=id)
    comments = post.comment_set.all()
    #handle comment form submit
    if request.method=="POST":
     
     body=request.POST.get("body")
    

     Comment.objects.create(post=post,user=request.user,body=body)

     return redirect('post_detail',id=post.id)




    return render(request,'blog/detail.html',{'post':post,'comments':comments})




#autentication
#register view
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            print("FORM VALID")
            return redirect('/')
        else:
            print("FORM INVALID")
            print(form.errors)

    else:
        form = RegisterForm()

    return render(request, 'blog/register.html', {'form': form})


@login_required
def like_post(request,post_id):
   post=get_object_or_404(Post,id=post_id)

   if request.user in post.likes.all():
      post.likes.remove(request.user)
   else:
      post.likes.add(request.user)

   return redirect(request.META.get('HTTP_REFERER','/'))      


@login_required
def delete_post(request,post_id):
   post=get_object_or_404(Post,id=post_id)

   if post.author==request.user:
      post.delete()


   return redirect('/')   


