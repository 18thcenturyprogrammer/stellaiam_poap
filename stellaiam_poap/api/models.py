import logging
from django.db import models
from django.utils import timezone

logger = logging.getLogger("mylogger")

def img_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    logger.info("filename is : ")
    logger.info(filename)

    filenameArr = filename.split(".")
    extenstion = filenameArr[len(filenameArr)-1]

    return 'imgs/{0}/{1}'.format(instance.email.replace("@","--").replace(".","_"), str(timezone.now().timestamp()).replace(".","")+'.'+extenstion)

def address_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    logger.info("filename is : ")
    logger.info(filename)

    filenameArr = filename.split("/")
    lastPart = filenameArr[len(filenameArr)-1]

    filenameArr2 = lastPart.split(".")
    extension = filenameArr2[len(filenameArr2)-1]

    return 'addresses/{0}/{1}'.format(instance.email.replace("@","--").replace(".","_"), str(timezone.now().timestamp()).replace(".","")+'.'+extension)


class DirectPoapClaim(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=200, blank=False, null=False)
    title =  models.CharField(max_length=200, blank=False, null=False)
    description =  models.CharField(max_length=1000, blank=False, null=False)
    image = models.ImageField(upload_to=img_path,blank=False, null = False)
    address = models.FileField(upload_to=address_path,blank=True, null = True)
    howMany = models.PositiveIntegerField(blank=False, null=False, default=1)


