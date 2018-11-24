#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytesseract
import fitz
import csv
import numpy as np
from skimage.color import rgb2gray
from PIL import Image
import _thread
import os
import glob
from skimage.io import imread
import json
from cmreslogging.handlers import CMRESHandler
import matplotlib.pyplot as plt
import logging
handler = CMRESHandler(hosts=[{'host': 'localhost', 'port': 32769}],
                           auth_type=CMRESHandler.AuthType.NO_AUTH,
                           es_index_name="tanzania2")
log = logging.getLogger("PythonTest")
log.setLevel(logging.INFO)
log.addHandler(handler)
'''
Pipeline for OCR:
1) Extract image from PDF file: https://github.com/rk700/PyMuPDF
2) Correct the skew to align the text (optional. Not implented yet).
3) Use tesseract to extract text with en+swa and save it inside a items.json file.
'''
data = []
def extract_images(pdf_filename):
    try:
        doc = fitz.open(pdf_filename)
        for elem in range(len(doc)):
            base_path, filename = os.path.split(pdf_filename)
            filename, file_extension = os.path.splitext(filename)
            png_filename_base = base_path + '/png/' + filename
            for img in doc.getPageImageList(elem):
                png_filename = png_filename_base+str(elem)+'.png'
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                if pix.n < 5:  # this is GRAY or RGB
                    pix.writePNG(png_filename)
                else:  # CMYK: convert to RGB first
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    pix1.writePNG(png_filename)
                    pix1 = None
                extract_text(png_filename)
    except:
        pass
def image_processing_pipeline(image):
    image = rgb2gray(image)
    image = 1 - (rgb2gray(np.asarray(image)) < 0.8)
    return Image.fromarray(image)
def extract_text(png_filename):
    img = imread(png_filename)
    img = image_processing_pipeline(img)
    text = pytesseract.image_to_string(img, lang='eng+swa')
    log.info({'value':text.strip(),'filename':png_filename})
    data.append({'text':text.strip()})

for pdf in glob.glob('D:/HIVHack/artverc/artverc/scrapers/data-artverc/data-gazette-tanzania/*.pdf'):
    extract_images(pdf)
#np.savetxt('./dataset.csv', data, delimiter=",")
with open('./dataset.json', 'w') as myfile:
    myfile.write(json.dumps(data))
