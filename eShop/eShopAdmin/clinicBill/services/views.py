from django.shortcuts import render,redirect
from services.models import Service
from services.forms import ServiceForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.conf import settings as conf_set
import xlwt
from xlwt.Formatting import Borders
# Create your views here.



sname=conf_set.C_NAME

# services Add View  
def services_addServ(request):
    if request.session.has_key('username'):
        lname=request.user.last_name 
        fname=request.user.first_name
        servicesData=Service.objects.all()
        if request.method == 'POST':
            service_form = ServiceForm(request.POST)
            if service_form.is_valid():
                try:
                    if Service.objects.filter(name__iexact=service_form.cleaned_data['name']).exists():
                        messages.error(request, 'Service Already Exist!')
                        return redirect('services_servAdd')
                    else:
                        service_model=Service()
                        service_model.name=service_form.cleaned_data['name']
                        service_model.price=service_form.cleaned_data['price']
                        service_model.save()
                        messages.success(request, 'Service Added Successfully!')
                        return redirect('services_servAdd')
                except:
                    messages.error(request,"Invalid header found in Add Service Form... Try again")
                    return redirect('services_servAdd')    
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            service_form = ServiceForm()
        context = {
            'sname':sname,
            'lname':lname,
            'page_title':" Services /",
            'fname':fname,
            "page_path":" Add Service",
            "menu_icon":"nav-icon fa fa-shopping-basket",
            "service_form":service_form,
            "servicesData":servicesData,
            }    
        return render(request, 'drviews/services.html',context) 
    else:
        return redirect('login') 




# Services Edit View
def services_editService(request,id):
    if request.session.has_key('username'):
        lname=request.user.last_name 
        fname=request.user.first_name
        servicesData=Service.objects.all()
        if request.method == 'POST':
            pi=Service.objects.get(pk=id)
            service_form = ServiceForm(request.POST,instance=pi)
            if service_form.is_valid():
                try:
                    service_form.save()
                    messages.success(request, 'Service Edited Successfully!')
                    return redirect('services_servAdd')
                except:
                    messages.error(request,"Invalid header found in Edit Service Form... Try again")
                    return redirect('services_servAdd')    
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            pi=Service.objects.get(pk=id)
            service_form = ServiceForm(instance=pi)
        context = {
            'sname':sname,
            'lname':lname,
            'page_title':" Services /",
            'fname':fname,
            "page_path":" Edit Service",
            "menu_icon":"nav-icon fa fa-shopping-basket",
            "service_form":service_form,
            "servicesData":servicesData,
            }    
        return render(request, 'drviews/services.html',context) 
    else:
        return redirect('login')





# Service Delete View
def services_delServ(request,id):
    if request.method == 'POST':
        pi=Service.objects.get(pk=id)
        pi.delete()
        messages.success(request, 'Service Deleted Successfully!')
        return redirect('services_servAdd')





# Service Export XlS View
def services_export_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="ServicesList.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('ServicesList')
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
    columns = ["Service ID","Service Name","Service Price"]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], excel_style)
    # Sheet body, remaining rows
    excel_style = xlwt.XFStyle()
    excel_style.borders = borders
    rows = Service.objects.all().values_list('id','name','price')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], excel_style)
    wb.save(response)
    return response

