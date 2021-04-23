from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .models import Employee
from .models import LeaveRequest
from .forms import EmployeeForm


# Create your views here.

def display(request):
    emp = Employee.objects.all()
    return render(request, "display.html", {'emp': emp})


def display_employee(request, empid):

    emp = Employee.objects.filter(employee_id=empid)
    context = {'emp': emp}
    return render(request, "display_employee.html", context)


def leave(request, empid):
    lv = LeaveRequest.objects.filter(employee_id=empid)
    emp = Employee.objects.filter(employee_id=empid)
    context = {
        'emp':emp,
        'LV': lv
      }
    return render(request, "displaytop2.html", context)


def add_employee(request):
    submitted = False
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('add_employee?submitted = True')
    else:
        form = EmployeeForm()
        if submitted in request.GET:
            submitted = True
        return render(request, 'add_employee.html', {'form': form, 'submitted': submitted})