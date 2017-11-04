from django.shortcuts import render,get_object_or_404
from .models import Post,Comment
from django.http import Http404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from .forms import CommentForm

class PostListView(ListView):
    queryset=Post.published.all()
    context_object_name='posts'
    paginate_by=3
    template_name='blog/post/list.html'
    
'''def post_list(request):
    object_list=Post.published.all()
    paginator=Paginator(object_list,3)#3 post eachpage
    page=request.GET.get('page')
    try:
        posts=paginator.page(page)
    except PageNotAnInteger:
        #If page is not an interger so deliver the first page
        posts=paginator.page(paginator.num_pages)
        return render(request,'blog/post/list.html',{'page':page,'posts':posts})
        posts=Post.published.all()
    return render(request,'blog/post/list.html',{'posts':posts})'''

def post_detail(request,year,month,day,post):
    '''post=get_object_or_404(Post,slug=post,status='published',publish__year=year,
                           publish__month=month,publish__day=day)'''
    try:
        post=Post.published.get(slug=post)
    except Post.DoesNotExist:
        raise Http404("Post Doesnot Exist")
    #list of active comments for the post
    comments=post.comments.filter(active=True)
    
    if request.method=='POST':
        comment_form=CommentForm(data=request.POST)
        #a comment was posted
        if comment_form.is_valid():
            #create comment object but dont save to database yet
            new_comment=comment_form.save(commit=False)
            #assign the current post to the comment
            new_comment.post=post
            #save the comment to database
            new_comment.save()
        else:
            comment_form=CommentForm()
    else:
        comment_form=CommentForm()
            
    return render(request,'blog/post/detail.html',{'post':post,'comments':comments,'comment_form':comment_form})
    '''return render(request,'blog/post/detail.html',{'post':post})'''

def post_share(request,post_id):
    #retrieve post by id
    post=get_object_or_404(Post,id=post_id,status='published')
    
    if request.method=='POST':
        #form was submitted
        form=EmailPostForm(request.POST)
        if form.is_valid():
            #form fields passed validation
            cd=form.cleaned_data

            #...send email
        else:
            form=EmailPostForm()
    return render(request,'blog/post/share.html',{'post':post,'form':form})
# Create your views here.
