from django.http import HttpResponse
from django.shortcuts import render
from basicapp.models import Patient
import pydicom  # for reading dicom files
import os  # for doing directory operations
import cv2
import numpy as np
import scipy.ndimage
import matplotlib.pyplot as plt
from matplotlib import pylab
from pylab import *
from zipfile import *
from pydicom.pixel_data_handlers.util import apply_voi_lut

import zipfile
import tempfile
import pdb
import imageio
import base64
import os
import time
import traceback
from io import BytesIO

import imageio
import matplotlib.pyplot as plt
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import redirect, render
from termcolor import colored
import png
from django.conf import settings
# Create your views here.


def index(request):
    patients = Patient.objects.all()
    return render(request, 'basicapp/patient_list.html', {'patients': patients})


def Examine(request, patient_id):

    # reading data
    # current path of app 'deepmodel'
    BASE = settings.BASE_DIR
    DICOM = settings.STATICFILES_DIRS[1]

    # get patient
    patient = Patient.objects.get(id=patient_id)

    # get PATIENT_DICOM of patient
    file = patient.PATIENT_DICOM

    # path of target directory to unzip
    target = os.path.join(BASE, 'DICOM\\'+str(patient.id) + '\\')

    # unzip directory
    with zipfile.ZipFile(file.path, 'r') as zip:
        path = zip.extractall(target)
    # get slices
    slices = []
    images = []
    for s in os.listdir(target + "PATIENT_DICOM\\"):
        Dicom_file = (target + "PATIENT_DICOM\\"+s)
        if not".png" in Dicom_file.lower():
            ds = pydicom.read_file(Dicom_file)
            slices.append(ds)
            path = target + "PATIENT_DICOM\\"+s
            shape = ds.pixel_array.shape
            image_2d = ds.pixel_array.astype(float)
            image_2d_scaled = (np.maximum(image_2d, 0) / image_2d.max()) * 255.0
            image_2d_scaled = np.uint8(image_2d_scaled)
            str1 = ""
            with open(path+'.png', 'wb') as png_file:
                w = png.Writer(shape[1], shape[0], greyscale=True)
                w.write(png_file, image_2d_scaled)
                image_path = (path + '.png').replace(DICOM, '')
                image_path = image_path.replace('\\', '', 1)
                dyaa = image_path
                #
                index = image_path.find('_')
                cnt = 0
                indx = index+1

                while indx:
                    if image_path[indx] == '.':
                        break
                    str1 = str1 + image_path[indx]
                    cnt += 1
                    indx += 1

                if cnt == 1:
                    image_path = image_path[:index+1] + '0' + str1 + ".png"

                images.append(image_path)

    images.sort()
    return render(request, 'png.html', {'images': images})

    # getting Hounsfield units
    # patient_pixels = get_pixels_hu(slices)

    # normalize patiens
    # normalized = normalize(patient_pixels)

    # resample
    # resampled = resample(patient_pixels, slices)

    # change datatype to float32
    # resampled = resampled.astype(np.float32)
    # resize patient to  number slices * 256 * 256
    # size = 256
    # pat = []
    # for num, each_slice in enumerate(resampled):
    # pat.append(cv2.resize(each_slice, (size, size)))


# returns the hounse fied unit of slices
def get_pixels_hu(slices):
    image = np.stack([s.pixel_array for s in slices])
    # Convert to int16 (from sometimes int16),
    # should be possible as values should always be low enough (<32k)
    image = image.astype(np.int16)

    # Set outside-of-scan pixels to 0
    # The intercept is usually -1024, so air is approximately 0
    image[image == -2000] = 0

    # Convert to Hounsfield units (HU)
    for slice_number in range(len(slices)):

        intercept = slices[slice_number].RescaleIntercept
        slope = slices[slice_number].RescaleSlope

        if slope != 1:
            image[slice_number] = slope * image[slice_number].astype(np.float64)
            image[slice_number] = image[slice_number].astype(np.int16)

        image[slice_number] += np.int16(intercept)

    return np.array(image, dtype=np.int16)


# normalize data withiin range -200 500
MIN_BOUND = -200.0
MAX_BOUND = 500.0


def normalize(image):
    image = (image - MIN_BOUND) / (MAX_BOUND - MIN_BOUND)
    image[image > 1] = 1.
    image[image < 0] = 0.
    return image

# resample the image to 1mm in all diminsions


def resample(image, slices, new_spacing=[1, 1, 1]):
    # Determine current pixel spacing
    spacing = np.array([slices[0].SliceThickness, slices[0].PixelSpacing[0],
                        slices[0].PixelSpacing[1]], dtype=np.float32)

    resize_factor = spacing / new_spacing
    new_real_shape = image.shape * resize_factor
    new_shape = np.round(new_real_shape)
    real_resize_factor = new_shape / image.shape
    new_spacing = spacing / real_resize_factor

    image = scipy.ndimage.interpolation.zoom(image, real_resize_factor, mode='nearest')
    return image
