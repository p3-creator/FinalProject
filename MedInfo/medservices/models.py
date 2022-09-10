from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    user_type = ((1,"Hospital"),(2,"Doctor"),(3,"Pharmacy"),(4,"BloodBank"),(5,"User"))
    user_type = models.CharField(default=1,choices=user_type,max_length=10)


class Hospital(models.Model):
     id=models.AutoField(primary_key=True)
     admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    # name = models.CharField(max_length=250)
     description = models.TextField()
     phone_number = models.TextField()
     district = models.CharField(max_length=250)
     address=models.CharField(max_length=250)
     website=models.CharField(max_length=250)
     specialities = models.TextField()
    #  email = models.CharField(max_length=250)
    #  password = models.CharField(max_length=50)
     objects=models.Manager()

     def __str__(self):
        return f"{self.name}" 


class Doctor(models.Model):
    id=models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    hospital_id = models.CharField(max_length=50)
    #hospital_id = models.ForeignKey(Hospital,on_delete=models.CASCADE,default=1)
    # first_name = models.CharField(max_length=60)
    # last_name = models.CharField(max_length=60)
    # doctor_name= models.CharField(max_length=100)
    nmc_number = models.CharField(max_length=50)
    education = models.TextField()
    # experience = models.TextField()
    speciality = models.TextField()
    # schedule = models.TextField()
    # email = models.CharField(max_length=250)
    # password = models.CharField(max_length=50)
    objects=models.Manager()
    #hospitals = models.ManyToManyField(Hospital, blank=False, related_name="doctors")

    # def __str__(self):
    #     return f"{self.first_name} {self.last_name}"

class Pharmacy(models.Model):
    id=models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    district = models.CharField(max_length=50)
    address = models.TextField()
    pranali = models.CharField(max_length=50)
    pharmacy_type = models.CharField(max_length=20)
    prescripton_type = models.CharField(max_length=10)
    website = models.TextField()
    objects = models.Manager()


class Blood_bank(models.Model):
    id=models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    # name = models.CharField(max_length=250)
    # email = models.CharField(max_length=250)
    # password = models.CharField(max_length=50)
    location = models.CharField(max_length=250)
    available_blood_groups = models.TextField()
    objects=models.Manager()

    def __str__(self):
        return f"{self.id}: {self.name} , {self.location} , {self.available_blood_groups}"

class User(models.Model):
    id=models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    # name = models.CharField(max_length=250)
    # email = models.CharField(max_length=250)
    # password = models.CharField(max_length=50)
    objects=models.Manager()

    def __str__(self):
        return f"{self.username}"

PAYMENT_STATUS = (
    ("paid","paid"),
    ("not paid","not paid"),
)

SPECIALITY_TYPE = (
    ("ear","ear"),
    ("eye","eye"),
    ("cardiology","cardiology"),
    
)

class Appointment(models.Model):
   # user = models.ForeignKey(User,on_delete=models.CASCADE)
    #hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    speciality = models.CharField(max_length=50,choices=SPECIALITY_TYPE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    pat_name = models.CharField(max_length=200)
    pat_address = models.CharField(max_length=200)
    pat_contact = models.IntegerField()
    #paid_amount = models.PositiveIntegerField()
    #payment_status = models.CharField(max_length=20,choices = PAYMENT_STATUS)
    objects = models.Manager()

    def __str__(self):
        return f"appointment with {self.doctor} of speciality {self.speciality}"


#Creating signal,This is called when data is added into customuser so new row can be added in hospital,doctor,user,bloodbank.
#creating @receiver so thsi method will run only when data added in customuser
@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            Hospital.objects.create(admin=instance)
        if instance.user_type==2:
            #Doctor.objects.create(admin=instance,hospital_id=Hospital.objects.get(id=1))
            Doctor.objects.create(admin=instance)
        if instance.user_type==3:
            Pharmacy.objects.create(admin=instance)
        if instance.user_type==4:
            Blood_bank.objects.create(admin=instance)
        if instance.user_type==5:
            User.objects.create(admin=instance)

@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
        if instance.user_type==1:
            instance.hospital.save()
        if instance.user_type==2:
            instance.doctor.save()
        if instance.user_type==3:
            instance.pharmacy.save()
        if instance.user_type==4:
            instance.blood_bank.save()
        if instance.user_type==5:
            instance.user.save()














