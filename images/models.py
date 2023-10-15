from django.db import models
import PIL
import numpy as np
from cvzone.SelfiSegmentationModule import SelfiSegmentation
from io import BytesIO
import os
from django.core.files.base import ContentFile
# Create your models here.
class Image(models.Model):
    img = models.ImageField( upload_to='images')
    rmbg_img = models.ImageField( upload_to='images_rmbg',blank=True)

    def __str__(self):
        return str(self.id)
    
    def save(self, *args,**kwargs):
        pil_img = PIL.Image.open(self.img)
        img = np.array(pil_img)
        segmentor = SelfiSegmentation()
        rmbg = segmentor.removeBG(img,(0,0,0),cutThreshold=0.4)
        buffer = BytesIO()
        output_img = PIL.Image.fromarray(rmbg)
        output_img.save(buffer,format="png")
        val = buffer.getvalue()
        filename = os.path.basename(self.img.name)
        name, _ =filename.split(".")
        self.rmbg_img.save(f"bgrm_{name}.png",ContentFile(val),save=False)
        super().save(*args,**kwargs)