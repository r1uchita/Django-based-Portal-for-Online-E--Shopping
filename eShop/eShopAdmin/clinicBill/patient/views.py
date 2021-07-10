from django.shortcuts import redirect,render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.conf import settings as conf_set
from patient.models import PatientRegister
from patient.forms import PRegistrationForm
import xlwt
from xlwt.Formatting import Borders
# Create your views here.

sname=conf_set.C_NAME

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def dashboard_dash(request):
    if request.session.has_key('username'):
        lname=request.user.first_name 
        fname=request.user.first_name
        context = {
            'sname':sname,
            'lname':lname,
            'page_title':" Dashboard",
            'fname':fname,
            "page_path":" / Dashboard",
            "menu_icon":"nav-icon fas fa-tachometer-alt"}
        return render(request,"drviews/dashboard.html",context) 
    else:
        return redirect('login') 




# Patient Register View  
def patient_register(request):
    if request.session.has_key('username'):
        lname=request.user.last_name 
        fname=request.user.first_name
        if request.method == 'POST':
            patient_form = PRegistrationForm(request.POST)
            if patient_form.is_valid():
                try:
                    if PatientRegister.objects.filter(mobile__iexact=patient_form.cleaned_data['mobile']).exists():
                        messages.error(request, 'Patient Already Exist!')
                        return redirect('patient_addp')
                    else:
                        patient_model=PatientRegister()
                        patient_model.name=patient_form.cleaned_data['name']
                        patient_model.dob=patient_form.cleaned_data['dob']
                        patient_model.gender=patient_form.cleaned_data['gender']
                        patient_model.mobile=patient_form.cleaned_data['mobile']
                        patient_model.email=patient_form.cleaned_data['email']
                        patient_model.address=patient_form.cleaned_data['address']
                        patient_model.photo=patient_form.cleaned_data['photo']
                        patient_model.save()
                        messages.success(request, 'Patient Registered Successfully!')
                        return redirect('patient_addp')
                except:
                    messages.error(request,"Invalid header found in Add Patient Register form... Try again")
                    return redirect('patient_addp')    
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            patient_form = PRegistrationForm()
        context = {
            'sname':sname,
            'lname':lname,
            'page_title':" Patient /",
            'fname':fname,
            "page_path":" Add Patient",
            "menu_icon":"nav-icon fa fa-address-card",
            "patient_form":patient_form,
            }    
        return render(request, 'drviews/patient.html',context) 
    else:
        return redirect('login') 




# Patient List View
def patient_listp(request):
    if request.session.has_key('username'):
        lname=request.user.last_name 
        fname=request.user.first_name
        patientRegisterData=PatientRegister.objects.all()
            #print(cy)
        context = {
            'sname':sname,
            'lname':lname,
            'page_title':" Patient  /",
            'fname':fname,
            "page_path":" List Patient",
            "menu_icon":"nav-icon fas fa-address-card",
            "patientRegisterData":patientRegisterData,    
            
            }    
        return render(request, 'drviews/patient_list.html',context) 
    else:
        return redirect('login') 





# Patient Edit View
def patient_editPatient(request,id):
    if request.session.has_key('username'):
        lname=request.user.last_name 
        fname=request.user.first_name
        #visitorData=Visitor.objects.all()
        if request.method == 'POST':
            pi=PatientRegister.objects.get(pk=id)
            patient_form = PRegistrationForm(request.POST,request.FILES,instance=pi)
            if patient_form.is_valid():
                try:
                    patient_form.save()
                    messages.success(request, 'Patient Edited Successfully!')
                    return redirect('patient_list')
                except:
                    messages.error(request,"Invalid header found in Edit Patient Form... Try again")
                    return redirect('patient_list')    
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            pi=PatientRegister.objects.get(pk=id)
            patient_form = PRegistrationForm(instance=pi)
        context = {
            'sname':sname,
            'lname':lname,
            'page_title':" Patient /",
            'fname':fname,
            "page_path":" Edit-Patient",
            "menu_icon":"nav-icon fas fa-address-card",
            "patient_form":patient_form,
            
            }    
        return render(request, 'drviews/patient.html',context) 
    else:
        return redirect('login')



# Patient Delete View
def patient_delpatient(request,id):
    if request.method == 'POST':
        pi=PatientRegister.objects.get(pk=id)
        pi.delete()
        messages.success(request, 'Patient Deleted Successfully!')
        return redirect('patient_list')




# Patient Export XlS View
def patient_export_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="PatientList.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('PatientList')
    # Sheet header, first row
    row_num = 0
    excel_style = xlwt.XFStyle()
    excel_style.font.bold = True
    borders = xlwt.Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1
    excel_style.borders = borders
    columns = ["Patient ID","Patient Name","Patient DOB","Patient Gender","Patient Mobile","Patient Email","Patient Address"]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], excel_style)
    # Sheet body, remaining rows
    excel_style = xlwt.XFStyle()
    excel_style.borders = borders
    rows = PatientRegister.objects.all().values_list('id','name','dob','gender','mobile','email','address')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], excel_style)
    wb.save(response)
    return response



