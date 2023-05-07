# Create your views here.
import cv2
import face_recognition
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
import face_recognition
from .models import MissingChild,AvailableChildPhotos


def index(request):
    return render(request, 'index.html')


def add_missing_child(request):
    availablePhotos =AvailableChildPhotos.objects.all()
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
            for availablePhoto in availablePhotos:
                if verify_faces(local_path,settings.MEDIA_ROOT+'/'+availablePhoto.photo.name):
                    messages.success(request, 'Child found')
                    return render(request, 'phot_search_results.html', {'child': child,'availablePhoto':availablePhoto})
                
            return render(request, 'phot_search_results.html')
        except Exception as e:
            print(e)
            messages.error(request, 'Error saving child')
            context['message'] = messages
            return redirect('report_missing')
    else:
        return render(request, 'add_missing_child.html', context)



def verify_faces(image_path_1, image_path_2):
    # Load the images of the two faces to compare
    image_1 = face_recognition.load_image_file(image_path_1)
    image_2 = face_recognition.load_image_file(image_path_2)

    # Get the face encodings for both images
    encodings_1 = face_recognition.face_encodings(image_1)
    encodings_2 = face_recognition.face_encodings(image_2)

    if len(encodings_1) > 0 and len(encodings_2) > 0:
        # Compare the first face encoding of each image to check if they belong to the same person
        results = face_recognition.compare_faces([encodings_1[0]], encodings_2[0])

        # Return the results
        if results[0]:
            return True
        else:
            return False
    else:
        return None
