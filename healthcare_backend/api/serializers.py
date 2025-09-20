from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Patient, Doctor, PatientDoctorMapping

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'email': {'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.get('username') or validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class PatientSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.id')

    class Meta:
        model = Patient
        fields = ['id','created_by','name','age','gender','address','phone','notes','created_at','updated_at']

    def validate_age(self, value):
        if value < 0: raise serializers.ValidationError("Age must be positive.")
        return value

class DoctorSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.id')
    class Meta:
        model = Doctor
        fields = ['id','created_by','name','specialization','email','phone','clinic','created_at']

class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    assigned_by = serializers.ReadOnlyField(source='assigned_by.id')
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all())

    class Meta:
        model = PatientDoctorMapping
        fields = ['id','patient','doctor','assigned_by','notes','created_at']

    def validate(self, data):
        # ensure patient belongs to requesting user
        request = self.context.get('request')
        if not request:
            return data
        patient = data.get('patient')
        if patient.created_by != request.user:
            raise serializers.ValidationError("You can only assign doctors to patients you created.")
        return data
