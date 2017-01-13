from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail
# Create your views here.
#in this view we retrieve the list of all the posts with the published status using our manager.

	
def post_detail(request, year, month, day, post):
	post = get_object_or_404(Post, slug=post, status='published', publish__year = year, publish__month=month, publish__day = day)
	return render(request, 'blog/post/detail.html', {'post':post})
	
"""
Steps : we instantiate the paginator class with the number of objects we want to display in each page
we get the page GET parameter that indicates the current page number
we obtain the objcts for the desired page by calling the page() method of the paginator.
if the page parameter is not an integer, we retrieve the first page of the results, if this parameter is a number greater than the last page of results, we retrieve the last page
we pass the page number and retrieved objects to the template
"""
def post_list(request):
	object_list = Post.published.all()
	paginator = Paginator(object_list, 3)
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)
	return render(request, 'blog/post/list.html', {'page':page, 'posts':posts})
	
def post_share(request, post_id):
	#retrieve post by id
	post = get_object_or_404(Post, id=post_id, status='published')
	sent = False
	
	if request.method == 'POST':
		#form was submitted
		form = EmailPostForm(request.POST)
		if form.is_valid():
			#form fields pased validation
			cd = form.cleaned_data
			#.... send the mail
			post_url = request.build_absolute_uri(post.get_absolute_url())
			subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
			message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
			send_mail(subject, message, 'admin@myblog.com',[cd['to']])
			sent = True
			
	else:
		form = EmailPostForm() #we create a new form instance that will be used to diaplay an empty form
	return render(request, 'blog/post/share.html', {'post':post, 'form':form, 'sent':sent})
		
"""
Notes on using the form - we use the same view to display the intial form and process the submitted data. we differentiate the form was submitted or not based on the request method. we are going to submit the form usng the post method. we assume that if we get the get request, an empt form has to be diplayed, and if we get a post request, the form has been submitted and needs to be processed.
"""
