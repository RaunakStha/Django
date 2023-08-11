from django.shortcuts import render,redirect
from .models import Blog,Contacts # manager objects
from .forms import BlogForm
from django.core.paginator import Paginator
from projectdemo.settings import EMAIL_HOST_USER #replace root with your project name
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.template.loader import render_to_string




# Create your views here.
def index(request):
    blog = Blog.objects.all()
    paginator = Paginator(blog,2)
    pages = request.GET.get('page')
    page_obj = paginator.get_page(pages)
    if(request.method == "POST"):
        searchData = request.POST.get("search")
        if(searchData != ""):
            data = Blog.objects.filter(title__icontains=searchData)
            return render(request,"crud/home.html",{'blogs':data})      
    return render(request,"crud/home.html",{"blogs":page_obj})


def about(request):
    return render(request,"crud/about.html")

def create(request):
    form = BlogForm(request.POST or None)
    if form.is_valid():
        form.save()
        return  redirect("crud:home")
    return render(request,"crud/createblog.html",{"form":form})

def deleteBlog(request,id):
    blog = Blog.objects.get(id=id)
    blog.delete()
    return redirect("crud:home")

def updateBlog(request,id):
    blog = Blog.objects.get(id=id)
    form = BlogForm(request.POST or None,instance=blog)
    if (form.is_valid()):
        form.save()
        return redirect("crud:home")
    context = {
        "form":form,
        "title":blog.title,
        "subheading":blog.subheading,
        "description":blog.description
    }
    return render(request,"crud/createblog.html",context)
    

def partData(request,id):
    blog = Blog.objects.get(id=id)
    print(blog)
    context = {
        "blog":blog
    }
    return render(request,"crud/particular.html",context)

def contacts(request):
    
    if(request.method == "POST"):
        dataName = request.POST.get("name")
        dataEmail = request.POST.get("email")
        dataMessage = request.POST.get("message")
        subject = "Wants to collaborate!!!"
        recipient = "heraldcollege@yopmail.com","np03cs4s220226@heraldcollege.edu.np",
        html_content = render_to_string('crud/email.html',{'name':dataName,'description':dataMessage,'mail':dataEmail})
        email=EmailMessage(
            subject,
            html_content,
            EMAIL_HOST_USER,
            recipient
        )
        email.fail_silently=False
        if email!=None:
            email.send()

       

        contacts = Contacts(
            name=dataName,
            email=dataEmail
        )

        contacts.save()
        print(dataName,dataEmail,dataMessage)
        # return redirect("crud:home")
      
           

    return render(request,"crud/contact.html")

def logoutuser (request):
    logout(request)
    return redirect ("crud:home")

def loginuser (request):
   
    if request.methode == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request, user)
            return("crud:home")
        else:
            return redirect("user/login.html")
        print(username,password)
    print(request.user)
    return redirect ("crud:home")

