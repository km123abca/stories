from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login,logout
import json
from .models import *

from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View
from django.shortcuts import get_object_or_404
from .forms import UserForm,UserFormLogin

# Create your views here.

def homepage(request):
	userLoggedIn=True if request.user.is_authenticated else False
	if request.session.has_key('has_message'):
		x=request.session['has_message']
		del request.session['has_message']
		return render(request,'stories/home.html',{'title':'Home Page',
												   'userLoggedIn':userLoggedIn,
												   'message':x,
												   }
					  )
	return render(request,'stories/home.html',{'title':'Home Page',
											   'userLoggedIn':userLoggedIn,
											   'message':'welcome to the homepage',
											   }
				 )

def startStory(request):
	userLoggedIn=True if request.user.is_authenticated else False
	
	return render(request,'stories/start_story.html',{'title':'Write your story','userLoggedIn':userLoggedIn})

def imageupload(request):
	userLoggedIn=True if request.user.is_authenticated else False
	if request.method=='GET':
		return redirect('startStory')
	if request.method=='POST' and request.FILES['filein']:
		myfile=request.FILES['filein']
		fs=FileSystemStorage()
		filename=fs.save(myfile.name,myfile)
		uploaded_file_url = fs.url(filename)
		return render(request,'stories/start_story.html',
								 {'title':'Write your story',
								  'uploaded_file_url': uploaded_file_url,
								  'userLoggedIn':userLoggedIn
								 }
					  )

def submitStory(request):
	if request.method=='POST':
		body_content=json.loads(request.body.decode('utf-8'))
		# print(body_content)
		componentList=json.loads(body_content["comps"])
		title=body_content["title"]
		genre=body_content["genre"]
		final=body_content["final"]
		final=True if final=='true' else False
		if request.user.is_authenticated:
			userx=request.user.username 
		else:
			userx="Guest"
			#TODO: Make sure that 2 guest users cant publish a story with the same name
		tex_name=userx+"-"+title.replace(" ","")
		story_s=Story.objects.all().filter(author=userx,title=title,genre=genre,textFileLocation=tex_name)
		if len(story_s)==0:
			story=Story(author=userx,title=title,genre=genre,textFileLocation=tex_name,finished=final)
		else:
			story=story_s[0]
			story.finished=final
			story.title=title
			story.genre=genre

		with open(".\\static\\media\\Textfiles\\"+tex_name+".txt","w+") as f:
			f.write('')
		
		with open(".\\static\\media\\Textfiles\\"+tex_name+".txt","a+") as f:
		# with open(userx+"-"+title.replace(" ","")+".txt","a+") as f:
			for x in componentList:
				if x["type"]=="textbox":
					f.write("\n"+"#startofstory#"+"\n")
					f.write(x["content"])
					f.write("\n"+"#endofstory#"+"\n")
				elif x["type"]=="image":
					f.write("\n"+"#startofimage#"+"\n")
					f.write(x["content"]);
					# f.write("\n"+x["width"]);
					f.write("\n"+"#endofimage#"+"\n")
		story.save()
		request.session['has_message']="story successfully submitted"
		return HttpResponse('{"msg":"ok"}')

def readStory(request,storyName,storyAuthor):
	userLoggedIn=True if request.user.is_authenticated else False
	storyx=Story.objects.all().filter(title=storyName,author=storyAuthor)[0]
	finFlag=storyx.finished
	storyGenre=storyx.genre
	#if not finFlag:
	#	print("The story,{storyName} was not finished ".format(storyName=storyName))
	try:
		f=open(".\\static\\media\\Textfiles\\"+storyAuthor+'-'+storyName.replace(' ','')+".txt","r")
		componentList=[]
		reading="none"
		strr=""
		# print(f.read())
		for i,line in enumerate(f.readlines()):		
			print("reading line:",i)
			if reading=="none":
				if '#startofstory#' in line:
					reading="textbox"
					strr=""
					continue
				
				elif '#startofimage#' in line:
					reading="image"
					strr=""
					continue
				
			elif '#endofstory#' in line: 
				reading="none"
				componentList.append({"type":"textbox","contents":strr.strip()})
				strr=""
				continue

			elif '#endofimage#' in line:
				reading="none"
				componentList.append({"type":"image","contents":strr})
				strr=""
				continue

			else:
				if reading=="textbox":
					strr+=line
				if reading=="image":
					strr+="/media/"+line.split('/')[-1]
		f.close()
		# return JsonResponse({"msg":"OK","componentList":componentList})
		if finFlag:
			return render(request,'stories/newStory.html',
								  {
								    "componentList":componentList,
								    'storyName':storyName,
			                   		'storyAuthor':storyAuthor,
			                   		'userLoggedIn':userLoggedIn
								  }
				         )
		else:
			return render(request,'stories/edit_Story.html',
							  {
							    "componentList":componentList,
							    'storyName':storyName,
		                   		'storyAuthor':storyAuthor,
		                   		'storyGenre':storyGenre,
		                   		'userLoggedIn':userLoggedIn
							  }
			         )
	except:
		return HttpResponse('{"msg":"Error opening file"}') 


def editStory(request,storyName,storyAuthor):
	try:
		f=open(".\\static\\media\\Textfiles\\"+storyAuthor+'-'+storyName.replace(' ','')+".txt","r")
		componentList=[]
		reading="none"
		strr=""
		# print(f.read())
		for i,line in enumerate(f.readlines()):		
			print("reading line:",i)
			if reading=="none":
				if '#startofstory#' in line:
					reading="textbox"
					strr=""
					continue
				
				elif '#startofimage#' in line:
					reading="image"
					strr=""
					continue
				
			elif '#endofstory#' in line: 
				reading="none"
				componentList.append({"type":"textbox","contents":strr.strip()})
				strr=""
				continue

			elif '#endofimage#' in line:
				reading="none"
				componentList.append({"type":"image","contents":strr})
				strr=""
				continue

			else:
				if reading=="textbox":
					strr+=line
				if reading=="image":
					strr+="/media/"+line.split('/')[-1]
		f.close()
		# return JsonResponse({"msg":"OK","componentList":componentList})
		return render(request,'stories/newStory.html',
							  {
							    "componentList":componentList,
							    'storyName':storyName,
		                   		'storyAuthor':storyAuthor,
							  }
			         )
	except:
		return HttpResponse('{"msg":"Error opening file"}')


def listOfStories(request):
	userLoggedIn=True if request.user.is_authenticated else False
	stories=Story.objects.all()
	return render(request,'stories/listofstories.html',
		                  {
		                   'stories':stories,	
		                   	'userLoggedIn':userLoggedIn                  
		                  }
		         )




#FORMS FOR LOGIN AND REGISTER
class LoginFormView(View):
    form_class=UserFormLogin
    template_name = 'stories/login.html'
    
    
    def get(self, request):        
        form = self.form_class(None)
        if request.session.has_key('askedfor'):
            return render(request, self.template_name, {'form': form,'title':'Login','err':'You have to Login First'})    
        return render(request, self.template_name, {'form': form,'title':'Login'})

    def post(self,request):
        form=self.form_class(request.POST)        
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(username=username,password=password)
            
            if user is not None and user.is_active:
                login(request,user)
                if request.session.has_key('askedfor'):
                    x=request.session['askedfor']
                    del request.session['askedfor']
                    return redirect(x)
                return redirect('homepage')
            return render(request, self.template_name, {'form': form,'title':'Login','error_message':'Wrong credentials'})
        
        return render(request, self.template_name, {'form': form,'title':'Login'})

class UserFormView(View):
    form_class = UserForm
    template_name = 'stories/register.html'

    def get(self, request):
        form = self.form_class(None)        
        return render(request, self.template_name, {'form': form,'title':'Register'})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # cleaned and normalized data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            if password!=password2:
            	return render(request, self.template_name, {'form': form,
            												'title':'Register',
            												'error_message':'Passwords not matching',
            												}
            				 )

            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user.is_active:
                # thats it.... User is logged in now, we can now refer to the user as request.user.username.etc
                login(request, user)
                if request.session.has_key('askedfor'):
                    x=request.session['askedfor']
                    del request.session['askedfor']
                    return redirect(x)
                return redirect('homepage')
            return render(request, self.template_name, {'form': form,'title':'Register','error_message':'Wrong credentials'})
        return render(request, self.template_name, {'form': form,'title':'Register','error_message':'LOGIN FAILED'})

def logout_user(request):
    logout(request)
    return redirect('login')




