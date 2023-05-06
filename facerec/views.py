# Create your views here.
import face_recognition
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import default_storage
from django.shortcuts import render

from .forms.Forms import PhotoSearchForm
from .models import MissingChild


def index(request):
    return render(request, 'index.html')


def photo_search(request):
    if request.method == 'POST':
        form = PhotoSearchForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_photo = form.cleaned_data['photo']
            # save uploaded photo to disk
            file_path = default_storage.save('tmp/photo.jpg', uploaded_photo)
            # load and encode uploaded photo
            uploaded_image = face_recognition.load_image_file(settings.MEDIA_ROOT + '/' + file_path)
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
            return render(request, 'phot_search_results.html', {'matches': matches})
    else:
        form = PhotoSearchForm()
    return render(request, 'photo_search.html', {'form': form})


def photo_searchw(request):
    if request.method == 'POST':
        form = PhotoSearchForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_photo = form.cleaned_data['photo']
            # save uploaded photo to disk
            file_path = default_storage.save('tmp/photo.jpg', uploaded_photo)
            # load and encode uploaded photo
            uploaded_image = face_recognition.load_image_file(settings.BASE_DIR + '/' + file_path)
            uploaded_encoding = face_recognition.face_encodings(uploaded_image)[0]
            # search for similar faces in the database
            children = MissingChild.objects.all()
            matches = []
            for child in children:
                image_path = str(child.photo)
                image = face_recognition.load_image_file(settings.BASE_DIR + '/' + image_path)
                encoding = face_recognition.face_encodings(image)[0]
                match = face_recognition.compare_faces([uploaded_encoding], encoding)[0]
                if match:
                    matches.append(child)
            # render results template
            return render(request, 'phot_search_results.html', {'matches': matches})
    else:
        form = PhotoSearchForm()
    return render(request, 'photo_search.html', {'form': form})


def add_missing_child(request):
    context = {}
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        date_of_birth = request.POST['date_of_birth']
        current_age = request.POST['current_age']
        gender = request.POST['gender']
        date_missing = request.POST['date_missing']
        photo = request.FILES['photo']
        child = MissingChild(first_name=first_name, last_name=last_name, date_of_birth=date_of_birth,
                             current_age=current_age, gender=gender, date_missing=date_missing, photo=photo)
        try:
            child.save()
            return render(request, 'index.html')
        except Exception as e:
            print(e)
            messages.error(request, 'Error saving child')
            return render(request, 'add_missing_child.html', context)
    else:
        return render(request, 'add_missing_child.html', context)