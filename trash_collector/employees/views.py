from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.apps import apps
from .models import Employee
from django.core.exceptions import ObjectDoesNotExist
from datetime import date, datetime
import calendar

# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.

@login_required
def index(request):
    # This line will get the Customer model from the other app, it can now be used to query the db for Customers
    Customer = apps.get_model('customers.Customer')
    logged_in_user = request.user
    try:
        # This line will return the customer record of the logged-in user if one exists
        logged_in_employee = Employee.objects.get(user=logged_in_user)
        
        todays_date = datetime.today()
        weekday_name=todays_date.strftime('%A')

        customers = Customer.objects.filter(zip_code=logged_in_employee.zip_code)
        today_customers = customers.filter(weekly_pickup=weekday_name)
        active_pickups = today_customers.exclude(suspend_start__lt=todays_date, suspend_end__gt=todays_date)

        context = {
            'logged_in_employee': logged_in_employee,
            'todays_date': todays_date,
            'active_pickups' : active_pickups,
        }
        return render(request, 'employees/index.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create'))

@login_required
def create(request):
    logged_in_user = request.user
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        new_employee = Employee(name=name_from_form, user=logged_in_user, address=address_from_form, zip_code=zip_from_form)
        new_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        return render(request, 'employees/create.html')
    
#edit function to edit an employee profile

@login_required
def edit_profile(request):
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        logged_in_employee.name = name_from_form
        logged_in_employee.address = address_from_form
        logged_in_employee.zip_code = zip_from_form
        logged_in_employee.save() 
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        context = {
            'logged_in_employee': logged_in_employee
        }
        return render(request, 'employees/edit_profile.html', context)

#confirm function to confirm pickups to have a charge of $20 to customer account. Also to confirm pickup.
@login_required
def confirm(request, customer_id):
    Customer = apps.get_model('customers.Customer')
    customer_from_db = Customer.objects.get(pk=customer_id)
    today = date.today()
    customer_from_db.date_of_last_pickup = today
    customer_from_db.balance += 20
    return HttpResponseRedirect(reverse('employees:index'))

@login_required
def filter_customers(request):
    Customer = apps.get_model('customers.Customer')
    customers = Customer.objects.filter(weekly_pickup='')
    context = {
            'customers':customers
        }
    return render(request, 'employees/index.html', context)
 

    
    
    
    # active_pickups.balance(20)
    # active_pickups.date_of_last_pickup(date.today)
    # active_pickups.save() 

    
# def my_function(para_one, para_two)
# my_function(5, 10)
# my_function(para_two=5, para_one=10)