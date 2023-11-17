from django.shortcuts import render
from firstapp.models import Post,Comment
from firstapp.forms import CommentForm
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
def index(request):
    posts=Post.objects.all()
    context={'posts':posts}
    return render(request,'index.html',context) 
class PostCreate(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','description','image']
    template_name='create.html'
    success_url='/'

def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
@login_required        
def detail(request,pk):
    p=Post.objects.get(pk=pk)
    comments=Comment.objects.filter(post_id=pk)
    # if this is a POST request we need to process the form data
    if request.method == "POST" :
        # create a form instance and populate it with data from the request:
        form = CommentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            comment=form.cleaned_data['comment']
            c=Comment(post_id=pk,comment=comment,user=request.user)
            c.save()
            comment=form.cleaned_data['comment']
            return HttpResponseRedirect((reverse('firstapp:detail',kwargs={'pk':pk})))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CommentForm()

    return render(request, "detail.html", {'form': form,'p':p,'comments':comments})


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect("/thanks/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, "name.html", {'form': form})    
