from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Patient, Doctor, PatientDoctorMapping
from .serializers import (RegisterSerializer, PatientSerializer, DoctorSerializer,
                          PatientDoctorMappingSerializer)
from .permissions import IsOwnerOrReadOnly

User = get_user_model()

# Registration view
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []  # allow anyone to register

# Optionally, you can use the builtin TokenObtainPairView for login (JWT)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Patients
class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        # Each user only sees their own patients
        return Patient.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        # Attach the logged-in user as created_by
        serializer.save(created_by=self.request.user)
        

# Doctors
class DoctorViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        # Return all doctors
        return Doctor.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# Patient-Doctor mapping
class PatientDoctorMappingViewSet(viewsets.GenericViewSet,
                                  generics.CreateAPIView,
                                  generics.ListAPIView,
                                  generics.DestroyAPIView):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PatientDoctorMapping.objects.all().order_by('-created_at')

    # POST -> create mapping (assign doctor to patient)
    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)

    # override list to optionally filter by patient_id query param
    def list(self, request, *args, **kwargs):
        patient_id = request.query_params.get('patient_id')
        if patient_id:
            qs = self.get_queryset().filter(patient_id=patient_id)
        else:
            qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    # For delete, can use the standard DestroyAPIView which requires pk
