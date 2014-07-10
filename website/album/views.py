import uuid
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect

from models import Album
from models import Photo
from models import PhotoDetail

class PhotoUploadForm(forms.Form):
    caption = forms.CharField(max_length=150)
    file = forms.FileField(required=True)
    
# Create your views here.

def s(request):
	pass
	
def album_main(request):
	return render(request, 'album.html', {
           
    })
    
    
def new_photo(request): # temp
	if request.method == "POST":
		form = PhotoUploadForm(request.POST, request.FILES)
		if form.is_valid():
			caption = form.cleaned_data['caption']
			file = request.FILES['file']
		
			uid = uuid.uuid1().hex
			file.name = uid
			
			details = PhotoDetail(file=file, width=0, height=0)
			details.save()
			photo = Photo(caption=caption, uuid=uid, details=details, author=request.user)	
			photo.save()
			
			return HttpResponseRedirect('/album')
	
	else:
		form = PhotoUploadForm()

	return render(request, 'new_photo.html', {
			'form': form,
	})