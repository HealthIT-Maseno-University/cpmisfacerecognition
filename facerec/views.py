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
    """Structural similarity in images refers to the degree of similarity
    or dissimilarity between two images based on their structural properties. Structural properties can include things like edge information, texture, and color, among others.

    One popular method for measuring structural similarity is the Structural SIMilarity (SSIM) index,
     which was developed as a metric to assess image quality. SSIM compares the structural information in two images by looking at local windows of pixels and calculating the mean, standard deviation, and covariance of these windows. The SSIM index ranges from -1 to 1, with 1 indicating perfect structural similarity and -1 indicating complete dissimilarity.

    Another method for measuring structural similarity is the Mean Structural Similarity (MSSIM) index, which is similar to SSIM but takes into account the average structural similarity across the entire image rather than just local windows.

    :param img1:
    :param img2:
    :return: ssim_score
    """
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
    """
The mean squared error is calculated by taking the difference between the predicted and actual values of a quantity, squaring the difference, and then taking the average of the squared differences across all samples. The formula for MSE is:

MSE = 1/n * sum((predicted - actual)^2)

where n is the number of samples in the dataset, predicted is the predicted value
for a given sample, and actual is the actual value for that sample.

MSE measures the average squared difference between the predicted and actual values,
 with larger differences contributing more to the final score. A smaller MSE indicates a better fit between the predicted and actual values, while a larger MSE indicates a worse fit.

MSE is commonly used as a loss function in machine learning algorithms,
where it is optimized during model training to minimize the difference between predicted and actual values.
    :param img1:
    :param img2:
    :return:
    """
    try:
        if img1.shape == img2.shape:
            mse_score = np.mean((img1 - img2) ** 2)
        else:
            mse_score = None
        return mse_score
    except:
        return 0


def compute_ncc_score(img1, img2):
    """
    Normalized cross-correlation (NCC) is a mathematical operation
     used to compare two signals or images by measuring the similarity between them. NCC is often used in image processing and computer vision applications, such as object recognition, image alignment, and stereo vision.

The NCC between two signals or images is calculated as the correlation
coefficient between them, normalized to a range between -1 and 1. The formula for NCC is:

NCC(x,y) = (1/n) * sum((x_i - mean(x)) * (y_i - mean(y)) / (std(x) * std(y)))

where x and y are the two signals or images being compared, n is the length of the signals or
the number of pixels in the images, mean(x) and mean(y) are the mean values of the signals or images, and std(x)
and std(y) are the standard deviations of the signals or images.

NCC is useful for comparing signals or images that may have differences in brightness or contrast,
since it normalizes the correlation coefficient by the standard deviations of the signals or images.
 NCC values closer to 1 indicate a high degree of
 similarity between the signals or images, while values closer to -1 indicate a high degree of dissimilarity.

In image processing, NCC is often used for template matching,
 where a template image is compared to a larger search image to find locations
  where the template appears in the search image. NCC can also be used for stereo vision,
   where the NCC between corresponding pixels in two stereo images is used to estimate the depth of objects in the scene.
    :param img1:
    :param img2:
    :return:
    """
    try:
        result = cv2.matchTemplate(img1, img2, cv2.TM_CCORR_NORMED)
        ncc_score = cv2.minMaxLoc(result)[1]
        return ncc_score
    except:
        return 0


def compute_histogram_score(img1, img2):
    """
    Histograms are a useful tool for visualizing and understanding the distribution of pixel values in an image.
     A histogram is a graph that shows the number of pixels for each possible value of a given range of values, or "bin"
     . For example,
     a histogram of pixel values in the range 0-255 would have 256 bins, one for each possible pixel value.
     The correlation coefficient ranges from -1 to 1,
     with 1 indicating a perfect positive correlation,
     0 indicating no correlation, and -1 indicating a perfect negative correlation.
    :param img1:
    :param img2:
    :return:
    """
    try:
        hist1 = cv2.calcHist([img1], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist2 = cv2.calcHist([img2], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        histogram_score = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
        return histogram_score
    except:
        return 0







