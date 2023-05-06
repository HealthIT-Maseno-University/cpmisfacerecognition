from rest_framework.authtoken import serializers

from facerec.models import MissingChild


class MissingChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissingChild
        fields = '__all__'
