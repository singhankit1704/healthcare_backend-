from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import PatientDoctorMapping
from .serializers import PatientDoctorMappingSerializer


class MappingListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        mappings = PatientDoctorMapping.objects.all()
        serializer = PatientDoctorMappingSerializer(mappings, many=True)
        return Response({"count": mappings.count(), "mappings": serializer.data})

    def post(self, request):
        serializer = PatientDoctorMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(assigned_by=request.user)
            return Response({
                "message": "Doctor assigned to patient successfully.",
                "mapping": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class MappingByPatientView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        mappings = PatientDoctorMapping.objects.filter(patient_id=patient_id)
        if not mappings.exists():
            return Response({
                "patient_id": patient_id,
                "message": "No doctors assigned to this patient.",
                "doctors": []
            })
        serializer = PatientDoctorMappingSerializer(mappings, many=True)
        return Response({
            "patient_id": patient_id,
            "count": mappings.count(),
            "mappings": serializer.data
        })


class MappingDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        mapping = get_object_or_404(PatientDoctorMapping, pk=pk)
        patient_name = mapping.patient.name
        doctor_name = mapping.doctor.name
        mapping.delete()
        return Response({
            "message": f"Dr. {doctor_name} has been unassigned from patient {patient_name}."
        }, status=status.HTTP_200_OK)
