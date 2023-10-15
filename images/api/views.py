from urllib import response
from wsgiref.util import FileWrapper
from rest_framework import viewsets
from .serializers import ImageSerializer
from ..models import Image
from django.http import HttpResponse
from rest_framework.decorators import action

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    # api/images/
    # api/images/<pk>


    @action(methods=['GET'],detail=True)
    # def download(self,request,pk):
    def download(self,*args,**kwargs):
        # api/images/<pk>/download/
        instance = self.get_object()
        img_path = instance.rmbg_img.path
        img = open(img_path,'rb')
        response = HttpResponse(FileWrapper(img),content_type="image/png")
        return response