from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from medservices.models import CustomUser
from django.db.models import Q

from medservices.EmailBackEnd import EmailBackEnd

from .models import Hospital, Doctor,User, Appointment_timeslots
from django.views.generic import View
from django.urls import reverse
from django.http import JsonResponse
import requests


# from django.views.generic import ListView, FormView
# from .appointment_forms import AvailabilityForm
# from  .appointment_function.availability import check_availability 



def frontpage(request):
      logged_in_user = None
      username =None
      if request.session.get('user_id'):
            logged_in_user = request.session.get('user_id')
            user = CustomUser.objects.get(id=logged_in_user)
            username = user.username
          

      return render(request,'frontpage.html',{'logged_in_user':logged_in_user,'username':username})


def homepage(request):
      logged_in_user = None
      username =None
      print(request.session.get('user_id'))
      if request.session.get('user_id'):
            logged_in_user = request.session.get('user_id')
            print(logged_in_user)
            user = CustomUser.objects.get(id=logged_in_user)
            username = user.username
      return render(request,'user_homepage.html',{'logged_in_user':logged_in_user,'username':username})

def user_profile(request):
      return render(request,'user_profile.html')

def user_profile_details(request):

       user = CustomUser.objects.get(id= request.session.get('user_id'))
      
       return render(request,'show_user_details.html',{'user':user})

def chooseregister(request):
      return render(request,'chooseregister.html')

def loginView(request):
      return render(request,'login.html')

def register_user(request):
      return render(request,'register_user.html')

def register_hospital(request):
      return render(request,'register_hospital.html')

def doRegister_hospital(request):
        if request.method != "POST":
            return HttpResponse("<h2>Method not allowed</h2>")
        else:
            name = request.POST.get("name")
            description = request.POST.get("description")
            phone = request.POST.get("phone")
            address = request.POST.get("address")
            district = request.POST.get("district")
            website = request.POST.get("website")

            # if request.POST.get('specialities')
            #    savedata = Hospital()
            #    savedata.specialities = request.POST.get('specialities')
            #    savedata.save()
            specialities = request.POST.get("specialities")
            email = request.POST.get("email")
            password = request.POST.get("password")
            cpassword = request.POST.get("cpassword")
            if  CustomUser.objects.filter(email=email).exists():
                    return HttpResponse("Email Already Exists!")
            else:
            
                  if password == cpassword:
                        user = CustomUser.objects.create_user(username=name,email=email,password=password,user_type=1)
                        user.hospital.description = description
                        user.hospital.phone_number = phone
                        user.hospital.specialities = specialities
                        user.hospital.address = address
                        user.hospital.district = district
                        user.hospital.website = website
                        user.save()
                        return HttpResponse("Successfully Registered")
                  else:
                        return HttpResponse("Password didn't match!!!")
          
                        
def doRegister_user(request):
        if request.method != "POST":
            return HttpResponse("<h2>Method not allowed</h2>")
        else:
            firstname = request.POST.get("firstname")
            lastname = request.POST.get("lastname")
            address = request.POST.get("address")
            username = request.POST.get("username")
            phone = request.POST.get("phone")
            email = request.POST.get("email")
            password = request.POST.get("password")
            cpassword = request.POST.get("cpassword")
           
            if  CustomUser.objects.filter(email=email).exists():
                    return HttpResponse("Email Already Exists!")
            else:
                  #if CustomUser.objects.filter(username=name , user_type = 5):
                  if CustomUser.objects.filter(username=username).count()>0:
                     return HttpResponse("Username Already Exists!!Try something new!")
                  else:

                        if password == cpassword:
                              user = CustomUser.objects.create_user(first_name=firstname,last_name=lastname,username=username,email=email,password=password,user_type=5)
                              user.user.address = address
                              user.user.phone = phone
                              user.save()
                              return HttpResponseRedirect("login/")
                        else: 
                              messages.error(request, 'Password didnt match!!!')
                              return HttpResponseRedirect("chooseregister/register_user/")      
                        

def doLogin(request):
      if request.method != "POST":
            return HttpResponse("<h2>Method not allowed</h2>")
      else:
             user=EmailBackEnd.authenticate(request,username= request.POST.get("email"), password = request.POST.get("password"))

             if user!=None:
               login(request,user)
              
              
           
              # return HttpResponse("Email : "+ request.POST.get("email")+ " Password:" + request.POST.get("password") + "usertype : "+request.user.user_type)
               
               if user.user_type == "1":
                   #print(user.id)
                   #current_user = request.session[request.user.id]
                   #user_name = user.username
                   #current_username=request.session['user_name']
                   #param={'current_user':current_user,'current_username':current_username}
                   #return render(request,'hospital/hospital_admin.html',param)   

                   request.session['hos_id'] = user.id
                   
                  #  request.session['uname'] =user.username
                  #  name=request.session['uname']
                  #  print(param)
                  #  print(name)
                  #  return HttpResponseRedirect("hospital_admin/",{"param":param,"name":name})  

                   return HttpResponseRedirect('hospital_admin/')
                  
                 
               if user.user_type== "2":
                         return HttpResponseRedirect("doctor_admin/")

               if user.user_type == "3":
                         return HttpResponseRedirect("pharmacy_admin/")

            #    if user.user_type==4:
            #             return HttpResponseRedirect('#')

               if user.user_type == "5":
                         request.session['user_id'] = user.id
                         return HttpResponseRedirect('/')      
                  
             else:
                   messages.error(request,"Invalid Login Details")
                   return HttpResponseRedirect('login/')
                 # return HttpResponse("Invalid Login")

def hospital_admin(request):
     
      return render(request,'hospital/hospital_admin.html')

def add_doctor(request,hos_id):
                hospital = Hospital.objects.get(admin=hos_id)
                spec = hospital.specialities
                context = {'speciality':spec.split(",")}

                return render(request,'doctor/add_doctor.html',context)

def add_doctor_save(request):
      if request.method != "POST":
            return HttpResponse("Method Not Allowed")
      else:
            nmc_number = request.POST.get("nmc_no")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            username = request.POST.get("uname")
            specialities = request.POST.get("category")
            education = request.POST.get("education")
            email = request.POST.get("email")
            password = request.POST.get("password")
            # try:
            user = CustomUser.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password,user_type=2)
            user.doctor.nmc_number=nmc_number
            user.doctor.hospital_id = request.session.get('hos_id')
            print(request.session.get('hos_id'))
            user.doctor.specialities=specialities
            print(user.doctor.specialities)
            user.doctor.education=education
            #user.doctor.hospital_id = Hospital.objects.get(hospital_id=instance)
            #user.doctor.hospital_id = request..hospital_id
            user.save()
            return HttpResponse("Successfully Added Doctor") 
            # except:
            #       return HttpResponse("Failed to Add Doctor")

def show_doctors(request):
       doctor = Doctor.objects.filter(hospital_id=request.session.get('hos_id'))
      # id = doctor.admin_id
       #user = CustomUser.objects.filter(id=id)
       return render(request,'doctor/show_doctors.html',{"doctors":doctor})
      
# def hospital(request, Hospital_id):
#      hospital = Hospital.objects.get(pk=Hospital_id)
#      return render(request, 'medservices/hospital.html', {
#            "hospitals" : hospital,
#             "docs": hospital.doctors.all()


def doctor_admin(request):
     return render(request,'doctor/doctor_admin.html')

def user_homepage(request):
   
           
      return render(request,'user_homepage.html')

def UserDetails(request):
      if request.user != None:
            return HttpResponse("User : "+request.user.email + "usertype : "+request.user.user_type)
      else:
            return HttpResponse("login First")

def logout_hospital(request):
      logout(request)
      return HttpResponseRedirect("/")

def logout_user(request):
      logout(request)
      return HttpResponseRedirect("/")

def search(request):
      if request.method != 'POST':
             return HttpResponse("<h2>Method Not Allowed</h2>") 
      else:
            loc = request.POST.get("location")
            category = request.POST.get("category")
            name   = request.POST.get("name")
            spec_type = request.POST.get("type")
            
            logged_in_user = None
            username =None
            if request.session.get('user_id'):
                  logged_in_user = request.session.get('user_id')
                  user = CustomUser.objects.get(id=logged_in_user)
           
      
            if   name != '' and spec_type != '':
                  
                
                        #    lookup = Q(specialities_icontains=spec_type)
                         #  print(lookups)
                           if category == 'Hospitals':
                              if CustomUser.objects.filter(username__icontains=name).exists():
                         
                                    admin = CustomUser.objects.get(username__icontains=name)
                                    lookups = Q(address__icontains=loc) & Q(admin__exact=admin)  & Q(specialities__icontains=spec_type)
                                 
                                    hos = Hospital.objects.filter(lookups)

                                    context = {
                                          'logged_in_user':logged_in_user,
                                          'hospitals':hos
                                    }      
                                    hos = Hospital.objects.filter(lookups)
                                    return render(request,'user_homepage.html',context)
                              else:
                                    context = {
                                          'result':"Search Failed.No such searches found!",
                                          'logged_in_user':logged_in_user
                                          }
                                    return render(request,'user_homepage.html',context)


                           elif category =='Doctors':
                              if CustomUser.objects.filter(username__icontains=name).exists():
                         
                                   admin = CustomUser.objects.filter(username__icontains=name)
                                   lookups =  Q(admin__icontainsA = admin) & Q(specialities__icontains=spec_type)
                             

                                   doc = Doctor.objects.filter(lookups)
                                   context = {
                                          'logged_in_user':logged_in_user,
                                          'doctors':doc
                                    } 
                                  
                               
                                  # hos = Hospital.objects.filter(admin = doc.hospital_id)
                                   #name = hos.admin.username
                                   return render(request,'user_homepage.html',context)
                              else:
                                    context = {
                                          'result':"Search Failed.No such searches found!",
                                          'logged_in_user':logged_in_user
                                          }
                                    return render(request,'user_homepage.html',context)

                  
                

            elif name != '':
                     
                     if  CustomUser.objects.filter(username__icontains = name).exists():
                         
                           admin = CustomUser.objects.get(username__icontains=name)
                           lookups = Q(address__icontains=loc) & Q(admin__exact=admin)  
                        #    lookup = Q(specialities_icontains=spec_type)
                        #    print(lookups)
                           hos = Hospital.objects.filter(lookups)

                           context = {
                                          'logged_in_user':logged_in_user,
                                          'hospitals':hos
                                    }   

                           #hos = Hospital.objects.filter(address=loc,admin=admin,specialities = spec_type)
                           return render(request,'user_homepage.html',context)
                     else:
                              context = {
                                    'logged_in_user':logged_in_user,
                                    'result':'No results match your search',

                                    }
                              return render(request,'user_homepage.html',context)
            
            elif spec_type != '':
                    
                           lookups = Q(address__icontains=loc) & Q(specialities__icontains=spec_type)
                        #    lookup = Q(specialities_icontains=spec_type)
                        #    print(lookups)
                           hos = Hospital.objects.filter(lookups)
                           context = {
                                          'logged_in_user':logged_in_user,
                                          'hospitals':hos
                                    } 
                           #hos = Hospital.objects.filter(address=loc,admin=admin,specialities = spec_type)
                           return render(request,'user_homepage.html',context)

            else:
                  context = {
                        'logged_in_user':logged_in_user,
                        'result':'No results match your search',

                  }
                  return render(request,'user_homepage.html',context)

                     
            # hos = Hospital.objects.filter(address=loc)
                  

def edit_doctor(request,doctor_id):
      doctor = Doctor.objects.get(admin = doctor_id)
      return render(request,'doctor/edit_doctor.html',{'doctor':doctor})
#      return HttpResponse(doctor_id)

def edit_doctor_save(request):
      if request.method != 'POST':
            return HttpResponse("<h2>Method Not Allowed</h2>")
      else:
            admin_id = request.POST.get("doctor_id")
            nmc_number = request.POST.get("nmc_no")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            username = request.POST.get("uname")
            speciality = request.POST.get("speciality")
            education = request.POST.get("education")
            email = request.POST.get("email")
            password = request.POST.get("password")
            try:
                  user = CustomUser.objects.get(id=admin_id)
                  user.first_name = first_name
                  user.last_name = last_name
                  user.username = username
                  user.email = email
                  user.password = password
                  user.save()

                  doctor = Doctor.objects.get(admin=admin_id)
                  doctor.nmc_number = nmc_number
                  doctor.speciality =speciality
                  doctor.education = education
                  doctor.save()

                  messages.success(request,"Successfully Editted Doctor Details")
                  return HttpResponseRedirect('hospital_admin/')   

            except:
                  messages.error(request,'Failed,Try again!')
                  return HttpResponseRedirect('hospital_admin/')    

def delete_doctor(request,doctor_id):
      doctor = Doctor.objects.get(admin = doctor_id)
      return render(request,'doctor/delete_doctor.html',{'doctor':doctor}) 
                

def delete_doctor_save(request):
    if request.method != 'POST':
            return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
            admin_id = request.POST.get("doctor_id")
            doctor = Doctor.objects.get(admin = admin_id)
            doctor.delete()
            messages.success(request,"Successfully Deleted Doctor")
            return HttpResponseRedirect('hospital_admin/')  

def manage_doc_timeslot(request,doctor_id):
        doctor = Doctor.objects.get(admin_id = doctor_id)
        return render(request, 'doctor/manage_doc_timeslot.html',{"doctor":doctor})

def save_doc_timeslot(request):
      start_time = request.POST.get("start_time")
      end_time = request.POST.get("end_time")
      time_slot = request.POST.get("time_slot")
      doctor_id = request.POST.get("d_id")
      doctor_object = Doctor.objects.get(admin = doctor_id)
    
      
      
      
      if end_time > start_time:
            appointment_timings = Appointment_timeslots.objects.create(start_time=start_time, end_time=end_time, time_slot=time_slot, doctor_id=doctor_object)
            appointment_timings.save()
            messages.success(request,"timing added successfully")
            return HttpResponseRedirect('/hospital_admin/') 
      else:
            messages.error(request,"Please check your end time and try again ")
            return  HttpResponseRedirect('/hospital_admin/manage_timeslot/'+doctor_id)



def appointment_form(request,h_id):
      patient_id = request.session.get('user_id')
      patient = User.objects.get(admin = patient_id)
      hospital = Hospital.objects.get(admin = h_id)
      specialities = hospital.specialities
      if Doctor.objects.filter(hospital_id = h_id).exists():
          doctor = Doctor.objects.filter(hospital_id = h_id)
          appointment_time = Appointment_timeslots.objects.all()

          print(appointment_time)
        
      else:
            doctor = 'None'
            appointment_time = 'None'

      context = {'hospital':hospital,'speciality_list':specialities.split(","),'doctor':doctor,'patient':patient, 'appointment_time':appointment_time}
      return render(request,"appointment_form.html",context)



# def appointment_form_save(request):
#       speciality = request.POST.get("category")
#       doctor = request.POST.get("doc_category")
#       name = request.POST.get("name")
#       address = request.POST.get("address")
#       phone = request.POST.get("phone")
#       total_amount =  request.POST.get("amount")
#       appointment = Appointment.objects.create(speciality=speciality,doctor=doctor,name=name,address=address,phone=phone,total_amount=total_amount)
#       appointment.save()
      
#       return redirect(reverse("khaltirequest") + "?appointment_id=" + str(appointment.id) )


def appointment_choosedatetime(request):
      patient_id = request.session.get('user_id')
      patient = User.objects.get(admin = patient_id)
      speciality = request.POST.get('category_spec')
      doctor_name = request.POST.get('select_sel_doc')
      hospital_id = request.POST.get('h_id')
    
      print(doctor_name)
      return HttpResponse("good")
      



class KhaltiRequestView(View):
      def get(self, request, *args, **kwargs):
            appointment_id = request.GET.get("appointment_id")
            appointment = Appointment.objects.get(id=appointment_id)
            context = {
                 "appointment":appointment
            }
            return render(request,"khaltirequest.html",context)



class KhaltiVerifyView(View):
      def get(self,request, *args, **kwargs):
            token = request.GET.get("token")
            amount = request.GET.get("total_amount")
            appointment_id = request.GET.get("appointment_id")
            print(token, amount, appointment_id)

            url = "https://khalti.com/api/v2/payment/verify/"
            payload = {
            "token": token,
            "amount": amount
            }
            headers = {
            "Authorization": "Key test_secret_key_66d939087cab49cf8b6efab1b4d1d61b"
            }

            appointment_obj = Appointment.objects.get(id = appointment_id)

            response = requests.post(url, payload, headers = headers)

            resp_dict = response.json()
            if resp_dict.get("idx"):
                  success = True
                  appointment_obj.payment_completed = True
                  appointment_obj.save()
            else:
                  success = False

            data = {
                  "success": success
            }
            return JsonResponse(data)









def pharmacy_admin(request):
     
      return render(request,'pharmacy/pharmacy_admin.html') 




# class DoctorList(ListView):
#       model=Doctor

# class AppointmentList(ListView):
#       model=Appointment

# class AppointmentView(FormView):
#       # def get(self, request, *args, **kwargs):
#       #       h_id = self.kwargs["h_id"]

#       form_class = AvailabilityForm
#       template_name = 'availability_form.html'

#       def form_valid(self, form):
#             data = form.cleaned_data
#             doctor_list = Doctor.objects.filter(speciality = data['speciality'])
#             available_doctors = []
#             for doctor in doctor_list:
#                   if check_availability(doctor,data['start_datetime'],data['end_datetime']):
#                         available_doctors.append(doctor)
#             if len(available_doctors)>0:          
#                   doctor = available_doctors[0]
#                   appointment = Appointment.objects.create(
#                         user = request.user,
#                         doctor = doctor,
#                         start_datetime = data['start_datetime'],
#                         end_datetime = data['end_datetime'],
#                         speciality = data['speciality'],
#                         pat_name = data['pat_name'],
#                         pat_address = data['pat_address'],
#                         pat_contact = data['pat_contact'],
#                   )
#                   appointment.save()
#                   return HttpResponse(appointment)
#             else:
#                   return HttpResponse("Appointment is not available.Please check at another time slot")

            















# def home(request):
#       return render(request, 'medservices/home.html',{} )


# def hospital(request, Hospital_id):
#      hospital = Hospital.objects.get(pk=Hospital_id)
#      return render(request, 'medservices/hospital.html', {
#            "hospitals" : hospital,
#             "docs": hospital.doctors.all()
#      })