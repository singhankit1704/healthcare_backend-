from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Doctor
from .serializers import DoctorSerializer


class DoctorListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        doctors = Doctor.objects.all()
        # Optional filter by specialization
        specialization = request.query_params.get('specialization')
        if specialization:
            doctors = doctors.filter(specialization=specialization)
        available = request.query_params.get('available')
        if available is not None:
            doctors = doctors.filter(is_available=available.lower() == 'true')

        serializer = DoctorSerializer(doctors, many=True)
        return Response({"count": doctors.count(), "doctors": serializer.data})

    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response({
                "message": "Doctor added successfully.",
                "doctor": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class DoctorDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        doctor = get_object_or_404(Doctor, pk=pk)
        serializer = DoctorSerializer(doctor)
        return Response({"doctor": serializer.data})

    def put(self, request, pk):
        doctor = get_object_or_404(Doctor, pk=pk, created_by=request.user)
        serializer = DoctorSerializer(doctor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Doctor updated successfully.",
                "doctor": serializer.data
            })
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        doctor = get_object_or_404(Doctor, pk=pk, created_by=request.user)
        doctor.delete()
        return Response({"message": "Doctor deleted successfully."}, status=status.HTTP_200_OK)
