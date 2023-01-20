import logging
logger = logging.getLogger("mylogger")
from django.core.exceptions import ValidationError

from django.conf import settings
from rest_framework import serializers

from api.models import DirectPoapClaim

# file size validation
# ref) https://www.codesnippet.dev/jvorcak/validating-image-dimensions-and-size-in-django-rest-framework
def file_size_validator(image):
    filesize = image.size

    print("file size is : ",filesize)
    

    if filesize > 10240000:
        raise ValidationError(f"You need to upload an image which is smaller than 10 mb")



class DirectPoapClaimSerializer(serializers.ModelSerializer):
    # django rest serializer method field
    # ref) https://www.django-rest-framework.org/api-guide/fields/#serializermethodfield
    # userObj = serializers.SerializerMethodField()

    class Meta:
        model = DirectPoapClaim
        fields =['id','email','title','description','image','address','howMany','imgCid','created']

    image = serializers.ImageField(validators=[file_size_validator], required=True)
    address = serializers.FileField(validators=[file_size_validator], required=True)
