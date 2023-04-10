from rest_framework import generics


class CRUD(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    pass