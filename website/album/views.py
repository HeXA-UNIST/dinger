import uuid
import mimetypes
import os.path
import json
from itertools import izip_longest

from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt


from django import forms
from django.contrib.auth.decorators import login_required
from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from models import Album
from models import Photo
from models import PhotoDetail

class PhotoUploadForm(forms.Form):
    caption = forms.CharField(max_length=150, required=False)
    file = forms.FileField(required=True)
    album = forms.CharField(widget=forms.HiddenInput(), initial=0)

def grouper(n, iterable, padvalue=None):
    return izip_longest(*[iter(iterable)]*n, fillvalue=padvalue)

def AjaxJsonResponse(data):
    return HttpResponse(json.dumps(data), content_type='application/json')
 
# Create your views here.

def response_image(path):
    wrapper = FileWrapper(file(path))
    mimetype = mimetypes.guess_type(path)[0]
    if mimetype == None:
        mimetype = 'image'
        
    response = HttpResponse(wrapper, mimetype=mimetype)
    return response

@login_required
def photo(request, photo_id):
    photo = Photo.objects.get(uuid=photo_id)
    return response_image(photo.details.file.path)
    
@login_required
def thumbnail(request, photo_id):
    
    photo = Photo.objects.get(uuid=photo_id)
    return response_image(photo.details.file.path)
    

@login_required
def album_main(request):
    return render(request, 'album.html', {
    })

    
@login_required
def new_photo(request): # temp
    if request.method == "POST":
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            caption = form.cleaned_data['caption']
            album_id = form.cleaned_data['album']
            file = request.FILES['file']
            
            ext = os.path.splitext(str(file))[1]
            uid = uuid.uuid1().time
            file.name = ''.join([str(uid), ext])
            
            details = PhotoDetail(file=file, width=0, height=0)
            details.save()
            
            album = None
            try:
                album = Album.objects.get(pk=album_id)
            except:
                pass
            print 'album_id', album_id
            print album
            photo = Photo(caption=caption, uuid=uid, details=details, album=album, author=request.user)  
            photo.save()
            
            return HttpResponseRedirect('/album')
    
    else:
        form = PhotoUploadForm()

    return render(request, 'new_photo.html', {
            'form': form,
    })
    

# ajax
def ajax_request_albums(request):
    print request.is_ajax()
    if not request.is_ajax():
        return HttpResponseRedirect('/album') 
    
    response_dict = {}
    albums = []
    for album in Album.objects.all():
        albums.append({
            'id': album.id,
            'name': album.name
        })
    response_dict.update({'status':0, 'albums': albums})
    return AjaxJsonResponse(response_dict)
    

def ajax_request_photos(request):
    #if not request.is_ajax():
    #    return HttpResponseRedirect('/album')     
    
    data = request.POST
    album_id = data.get('album', 0)
    next = data.get('next', 0)
    
    response_dict = {}
    
    try:
        album_id = int(album_id)
    except:
        album_id = 0;

    try:
        next = int(next)
    except:
        next = 0;
    
    if album_id == 0:
        query = Photo.objects.all()
    else:
        album = None
        try:
            album = Album.objects.get(pk=album_id)    
        except:
            pass

        if album is None:
            response_dict.update({'status': -1})
            return AjaxJsonResponse(response_dict)
        # @logic => check album accessible
        query = Photo.objects.filter(album=album)

    # @logic => next filter
    if next > 0:
        query = query.filter(uuid__lt=next)

    result_dict = {}
    photo_data = []

    NUM_PHOTO = 20
    num_left = len(query)
    next_uuid = 0
    for photo in query.order_by('-uuid')[:NUM_PHOTO]:
        photo_data.append({
            'caption': photo.caption,
            't_url': reverse('thumbnail', args=[photo.uuid]),
            'url': reverse('photo', args=[photo.uuid]),
        })
        
        next_uuid = photo.uuid
        num_left = num_left - 1

    result_dict.update({
        'size': len(photo_data),
        'photos': photo_data,
        'next': str(next_uuid),
        'left_size': num_left
    })

    response_dict.update({'status':0, 'result': result_dict})
    return AjaxJsonResponse(response_dict)
