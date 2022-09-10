import datetime 
from medservices.models import Hospital,Doctor,Appointment

def check_availability(doctor,start_datetime,end_datetime):
    avail_list = []
    appointment_list = Appointment.objects.filter(doctor=doctor)
    for appointment in appointment_list:
       
            if appointment.start_datetime > end_datetime or appointment.end_datetime < start_datetime:
                avail_list.append(True)
            else:
                avail_list.append(False)
       
    return all(avail_list)