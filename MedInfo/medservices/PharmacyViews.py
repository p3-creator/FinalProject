from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from medservices.models import CustomUser


from medservices.EmailBackEnd import EmailBackEnd
from .models import Pharmacy


def register_pharmacy(request):
    return render(request,'pharmacy/register_pharmacy.html')

def doRegister_pharmacy(request):
        if request.method != "POST":
            return HttpResponse("<h2>Method not allowed</h2>")
        else:
            name = request.POST.get("name")
            district = request.POST.get("district")
            address = request.POST.get("address")
            prescription_type= request.POST.get("prescription_type")
            pharmacy_type = request.POST.get("type")
            phone = request.POST.get("phone")
            email = request.POST.get("email")
            password = request.POST.get("password")
            cpassword = request.POST.get("cpassword")
           
            if  CustomUser.objects.filter(email=email).exists():
                    return HttpResponse("Email Already Exists!")
            else:
                  #if CustomUser.objects.filter(username=name , user_type = 5):
                  if CustomUser.objects.filter(username=name).count()>0:
                     return HttpResponse("Username Already Exists!!Try something new!")
                  else:

                        if password == cpassword:
                              user = CustomUser.objects.create_user(username=name,email=email,password=password,user_type=3)
                              user.pharmacy.address = address
                              user.pharmacy.district = phone
                              user.pharmacy.prescription_type = prescription_type
                              user.pharmacy.pharmacy_type = pharmacy_type
                              user.pharmacy.phone = phone
                              user.save()
                              return HttpResponseRedirect("login/")
                        else: 
                              messages.error(request, 'Password didnt match!!!')
                              return HttpResponseRedirect("chooseregister/register_user/")  
    