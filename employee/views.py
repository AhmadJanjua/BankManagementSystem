from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from department.models import Department
from .models import Employee

@login_required
def create_employee(request):
    if not request.user.is_superuser:
        return redirect('home')
    error = None
    if request.method == 'POST':
        employee_type = request.POST.get('employee_type')
        id = request.POST.get('id')
        password = request.POST.get('password')
        ssn = request.POST.get('ssn')
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        birthday = request.POST.get('birthday')
        street = request.POST.get('street')
        city = request.POST.get('city')
        province = request.POST.get('province')
        postal_code = request.POST.get('postal_code')
        dept_id = request.POST.get('dept')
        try:
            dept = Department.objects.get(DNO=dept_id)
        except Department.DoesNotExist:
            dept = None
        if not id or not password or not ssn or not f_name or not l_name or not birthday or not street or not city or not province or not postal_code or not dept:
            error = 'All fields are required'
        elif employee_type == 'advisor':
            cpf_num = request.POST.get('cpf_num')
            office_num = request.POST.get('office_num')
            if not cpf_num or not office_num:
                error = 'All fields are required for an advisor account'
            else:
                User = get_user_model()
                User.objects.create_advisor(password=password, ssn=ssn, f_name=f_name, l_name=l_name, birthday=birthday,
                                            street=street, city=city, province=province, postal_code=postal_code, dept=dept,
                                            cpf_num=cpf_num, office_num=office_num)
                return redirect('home')
        elif employee_type == 'teller':
            User = get_user_model()
            User.objects.create_teller(ssn=ssn, f_name=f_name, l_name=l_name, birthday=birthday, street=street, city=city,
                                        province=province, postal_code=postal_code, dept=dept, password=password)
            return redirect('home')
        elif employee_type == 'manager':
            User = get_user_model()
            User.objects.create_manager(password=password, ssn=ssn, f_name=f_name, l_name=l_name, birthday=birthday,
                                        street=street, city=city, province=province, postal_code=postal_code, dept=dept)
            return redirect('home')
    departments = Department.objects.all()
    return render(request, 'create_employee.html', {'departments': departments, 'error': error})

def manage_employees(request):
    department_managed = Department.objects.filter(dept_mgr=request.user)
    Dnos = department_managed.values('DNO')
    Dn = Dnos[0]
    Rez = Dn.get('DNO')
    employees = Employee.objects.filter(is_staff=True,dept=Rez).exclude(is_superuser=True, manager__isnull=False)
    return render(request, 'manage_employees.html', {'employees': employees})
