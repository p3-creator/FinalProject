from django.urls import path
from . import views

urlpatterns = [
    path('', views.frontpage, name='medservice-frontpage'),
    path('homepage',views.homepage,name='homepage'),
    path('user_profile',views.user_profile,name='userprofile'),
    path('search_options',views.search,name='search'),
    path('chooseregister/', views.chooseregister,name='medservice-regchoice'),
    path('login/', views.loginView,name='medservice-login'),
    path('doLogin', views.doLogin),
    path('chooseregister/register_user/',views.register_user),
    path('chooseregister/register_user/login/',views.loginView),
    path('chooseregister/register_hospital/',views.register_hospital),
    path('chooseregister/register_hospital/login/',views.loginView),
    path('doRegister_hospital',views.doRegister_hospital),
    path('doRegister_user',views.doRegister_user),
    path('hospital_admin/add_doctor',views.add_doctor),
    path('hospital_admin/show_doctors',views.show_doctors),
    path('hospital_admin/',views.hospital_admin),
    path('doctor_admin/',views.doctor_admin),
    path('add_doctor_save',views.add_doctor_save),
    path('edit_doctor_save',views.edit_doctor_save),
    path('hospital_admin/edit_doctor/<str:doctor_id>',views.edit_doctor),
    path('hospital_admin/delete_doctor/<str:doctor_id>',views.delete_doctor),
    path('delete_doctor_save',views.delete_doctor_save),
    path('user_homepage/',views.user_homepage),
    path('get_user_detail',views.UserDetails),
    path('logout_user',views.logout_user),
    path('hospital_admin/logout_hospital',views.logout_hospital)



        # path('<int:Hospital_id>', views.hospital, name='medservice-hospital'),
   

]