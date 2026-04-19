from rest_framework import serializers
from .models import PatientDoctorMapping
from patients.models import Patient
from doctors.models import Doctor


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    patient_id = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(), source='patient', write_only=True
    )
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(), source='doctor', write_only=True
    )
    patient = serializers.SerializerMethodField(read_only=True)
    doctor = serializers.SerializerMethodField(read_only=True)
    assigned_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = ['id', 'patient_id', 'doctor_id', 'patient', 'doctor',
                  'notes', 'assigned_by', 'assigned_at']
        read_only_fields = ['id', 'patient', 'doctor', 'assigned_by', 'assigned_at']

    def get_patient(self, obj):
        return {"id": obj.patient.id, "name": obj.patient.name, "age": obj.patient.age}

    def get_doctor(self, obj):
        return {
            "id": obj.doctor.id,
            "name": obj.doctor.name,
            "specialization": obj.doctor.get_specialization_display(),
        }

    def get_assigned_by(self, obj):
        return {
            "id": obj.assigned_by.id,
            "name": f"{obj.assigned_by.first_name} {obj.assigned_by.last_name}".strip(),
        }

    def validate(self, attrs):
        patient = attrs.get('patient')
        doctor = attrs.get('doctor')
        if PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor).exists():
            raise serializers.ValidationError(
                f"Doctor '{doctor.name}' is already assigned to patient '{patient.name}'."
            )
        return attrs
