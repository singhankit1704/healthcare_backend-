from rest_framework import serializers
from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField(read_only=True)
    specialization_display = serializers.CharField(source='get_specialization_display', read_only=True)

    class Meta:
        model = Doctor
        fields = [
            'id', 'name', 'specialization', 'specialization_display', 'email',
            'contact_number', 'license_number', 'experience_years', 'qualification',
            'hospital', 'is_available', 'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'specialization_display', 'created_at', 'updated_at']

    def get_created_by(self, obj):
        return {
            "id": obj.created_by.id,
            "name": f"{obj.created_by.first_name} {obj.created_by.last_name}".strip(),
        }

    def validate_experience_years(self, value):
        if value < 0:
            raise serializers.ValidationError("Experience years cannot be negative.")
        return value
