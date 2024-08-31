from rest_framework import generics

from .models import AreaMaster, ExampleModel
from .serializers import AreaMasterSerializer, ExampleModelSerializer


class ExampleModelListCreateAPIView(generics.ListCreateAPIView):
    queryset = ExampleModel.objects.all()
    serializer_class = ExampleModelSerializer


class ExampleModelRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExampleModel.objects.all()
    serializer_class = ExampleModelSerializer


class AreaMasterListCreateAPIView(generics.ListCreateAPIView):
    queryset = AreaMaster.objects.all()
    serializer_class = AreaMasterSerializer


# class AreaMasterRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = AreaMaster.objects.all()
#     serializer_class = AreaMasterSerializer
