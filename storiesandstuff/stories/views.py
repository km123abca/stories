from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login,logout
import json
from .models import *

# Create your views here.

def homepage(request):
	return render(request,'stories/home.html',{'title':'Home Page'})

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
		if request.user.is_authenticated:
			userx=request.user.username 
		else:
			userx="Guest"
			#TODO: Make sure that 2 guest users cant publish a story with the same name
		tex_name=userx+"-"+title.replace(" ","")
		story=Story(author=userx,title=title,genre=genre,textFileLocation=tex_name)
		
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
		return HttpResponse('{"msg":"ok"}')

def readStory(request,storyName,storyAuthor):
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
	stories=Story.objects.all()
	return render(request,'stories/listofstories.html',
		                  {
		                   'stories':stories,		                   
		                  }
		         )

	


