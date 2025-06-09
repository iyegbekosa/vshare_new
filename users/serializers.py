from rest_framework import serializers
from .models import User, DriverProfile

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ('email', 'password', 'phone', 'first_name', 'last_name')
        extra_kwargs = {'password':{'write_only':'True'}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class RegisterDriverSerializer(serializers.ModelSerializer):
    license_number = serializers.CharField()
    plate_number = serializers.CharField()
    vehicle_color = serializers.CharField(required=False)
    vehicle_year = serializers.IntegerField(required=False)
    vehicle_type = serializers.CharField()
    vehicle_model = serializers.CharField()
    documents = serializers.FileField()

    class Meta:
        model = User
        fields = (
            'email', 'password', 'phone',
            'first_name', 'last_name', 'license_number',
            'plate_number', 'vehicle_color', 'vehicle_year',
            'vehicle_type', 'vehicle_model', 'documents'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        driver_fields = {
            'license_number': validated_data.pop('license_number'),
            'plate_number': validated_data.pop('plate_number'),
            'vehicle_color': validated_data.pop('vehicle_color', ''),
            'vehicle_year': validated_data.pop('vehicle_year', None),
            'vehicle_type': validated_data.pop('vehicle_type'),
            'vehicle_model': validated_data.pop('vehicle_model'),
            'documents': validated_data.pop('documents'),
        }

        user = User.objects.create_user(
            **validated_data,
            role='driver'
        )

        DriverProfile.objects.create(user=user, **driver_fields)

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'user_name', 'first_name', 'last_name', 'phone', 'role', 'is_active']