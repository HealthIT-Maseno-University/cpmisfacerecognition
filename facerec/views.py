# Create your views here.
import cv2
import face_recognition
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect

from .models import MissingChild


def index(request):
    return render(request, 'index.html')


def add_missing_child(request):
    context = {}
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        gender = request.POST['gender']
        photo_uploaded = request.FILES['photo']
        if photo_uploaded is None:
            messages.error(request, 'Please select a photo.')
            return redirect('report_missing')
        photo = default_storage.save('missing_children/' + photo_uploaded.name, photo_uploaded)
        local_path = default_storage.path(photo)
        with open(local_path, 'wb') as f:
            f.write(photo_uploaded.read())
        child = MissingChild(first_name=first_name, last_name=last_name, photo=photo, gender=gender)
        try:
            child.save()
            return render(request, 'phot_search_results.html')
        except Exception as e:
            print(e)
            messages.error(request, 'Error saving child')
            context['message'] = messages
            return redirect('report_missing')
    else:
        return render(request, 'add_missing_child.html', context)


def checkResemblance(images,filename):
    # load and encode uploaded photo
    uploaded_image = face_recognition.load_image_file(settings.MEDIA_ROOT + '/' + filename)
    uploaded_encoding = face_recognition.face_encodings(uploaded_image)[0]
    # search for similar faces in the database
    children = MissingChild.objects.all()
    matches = []
    for child in children:
        image_path = str(child.photo)
        image = face_recognition.load_image_file(settings.MEDIA_ROOT + '/' + image_path)
        encoding = face_recognition.face_encodings(image)[0]
        match = face_recognition.compare_faces([uploaded_encoding], encoding)[0]
        if match:
            matches.append(child)
    # render results template
    return matches

