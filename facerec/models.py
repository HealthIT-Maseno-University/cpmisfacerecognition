import cv2
import numpy as np
from django.db import models
from tensorflow.python.ops.image_ops_impl import ssim


# Create your models here.
class Child(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=8)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class MissingChild(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='missing_children')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class AvailableChildPhotos(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='available_photos')
    photo = models.ImageField(upload_to='available_children')

    def __str__(self):
        return f"{self.photo.name}"


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
