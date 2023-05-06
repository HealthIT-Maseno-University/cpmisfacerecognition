# Create your views here.
import face_recognition
from django.conf import settings
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
            return render(request, 'missing_children/photo_search_results.html', {'matches': matches})
    else:
        form = PhotoSearchForm()
    return render(request, 'missing_children/photo_search.html', {'form': form})
