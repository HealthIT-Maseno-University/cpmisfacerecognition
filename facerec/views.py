# Create your views here.
import cv2
import face_recognition
import numpy as np
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from tensorflow.python.ops.image_ops_impl import ssim

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


def compute_ssim_score(img1, img2):
    
    try:
        win_size = min(img1.shape[:2])
        win_size = (win_size // 2) * 2 + 1  # Ensure odd window size
        sigma = 1.5 * win_size / 11
        if img1.ndim > 2:
            channel_axis = 2
        else:
            channel_axis = None
        ssim_score = ssim(img1, img2, win_size=win_size, sigma=sigma, multichannel=True, channel_axis=channel_axis)
        return ssim_score
    except:
        return 0


def compute_mse_score(img1, img2):
    try:
        if img1.shape == img2.shape:
            mse_score = np.mean((img1 - img2) ** 2)
        else:
            mse_score = None
        return mse_score
    except:
        return 0


def compute_ncc_score(img1, img2):
    try:
        result = cv2.matchTemplate(img1, img2, cv2.TM_CCORR_NORMED)
        ncc_score = cv2.minMaxLoc(result)[1]
        return ncc_score
    except:
        return 0


def compute_histogram_score(img1, img2):
    try:
        hist1 = cv2.calcHist([img1], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist2 = cv2.calcHist([img2], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        histogram_score = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
        return histogram_score
    except:
        return 0







