from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
from blogs.models import Post,Comment
from django.utils import timezone
from blogs.forms import PostForm,CommentForm
from django.urls import reverse_lazy
# Create your views here.

class Aboutview(TemplateView):

    template_name='aboutpage.html'

class PostListView(ListView):
    # context_object_name='posting'
    model=Post

    # template_name='post_list.html'
    def get_queryset(self):
        return Post.objects.filter(publishtime__lte=timezone.now()).order_by('-publishtime')

class PostDetailView(DetailView):
    # context_object_name='posts'
    model=Post



class CreatePostView(LoginRequiredMixin,CreateView):
    # context_object_name='posting'
    login_url='/login/'
    redirect_field_name='blogs/post_detail.html'
    form_class=PostForm
    model=Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url='/login/'
    redirect_field_name='blogs/post_detail.html'
    form_class=PostForm
    model=Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model=Post

    success_url=reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin,ListView):
    # context_object_name='postsii'
    login_url='/login/'
    redirect_field_name='blogs/post_list.html'
    model=Post


    def get_queryset(self):
        return Post.objects.filter(publishtime__isnull=True).order_by('createtime')


@login_required
def post_publish(request,pk):
    publish=get_object_or_404(Post,pk=pk)
    publish.publishpost()
    return redirect('post_detail',pk=pk)


@login_required
def add_comment_to_post(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            #Here Model CommentPost has ForeignKey Known as Post. SO that Comment can be added to that particular post.
            comment.post=post
            comment.save()
            redirect('post_detail',pk=post.pk)
    else:
        form=CommentForm()
    return render(request,'blogs/comment_form.html',{'form':form})

@login_required
def comment_approve(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)


@login_required
def comment_remove(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    pk_post=comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=pk_post)
