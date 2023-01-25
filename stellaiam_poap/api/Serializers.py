import logging
logger = logging.getLogger("mylogger")
from django.core.exceptions import ValidationError

from django.conf import settings
from rest_framework import serializers

from api.models import PoapClaim

# file size validation
# ref) https://www.codesnippet.dev/jvorcak/validating-image-dimensions-and-size-in-django-rest-framework
def file_size_validator(image):
    filesize = image.size

    print("file size is : ",filesize)
    

    if filesize > 10240000:
        raise ValidationError(f"You need to upload an image which is smaller than 10 mb")



class PoapClaimSerializer(serializers.ModelSerializer):
    # django rest serializer method field
    # ref) https://www.django-rest-framework.org/api-guide/fields/#serializermethodfield
    # userObj = serializers.SerializerMethodField()
    secret = serializers.CharField(write_only=True, required = False)

    class Meta:
        model = PoapClaim
        fields =['id','email','title','description','image','address','howMany','imgCid', 'metaCid','created', 'secret', 'paidTxHash', 'uriTxHash', 'whoPaid', 'updated', 'isPaid']

        # # make it not required
        # # ref) https://stackoverflow.com/a/46842288
        # extra_kwargs = {'secret': {'required': False}}
   