from django.shortcuts import render, redirect
from django.views.generic import CreateView,UpdateView,ListView,DeleteView
from .forms import EmployeeAddressForm
from .models import Employee, EntryRecord, EntrySchedule, DisciplineRecord
from django.utils import timezone
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta

# class EmployeeCreateView(CreateView):
#     model = Employee
#     fields = []
#     template_name = 'address_form.html'
#     success_url = reverse_lazy('employee:employee_list')  
    
class CreateEmployeeAddressView(CreateView):
    template_name = 'template.html'
    form_class = EmployeeAddressForm
    success_url = reverse_lazy('customers:customer_detail')  # Reemplaza 'nombre_de_la_vista_de_exito'

    def form_valid(self, form):
        # Guardar el formulario sin commit para obtener el cliente
        customer = form.save(commit=False)
        customer.save()

        # Obtener la instancia de Address del formulario
        address = form.cleaned_data.get('address')  # Asegúrate de que este sea el nombre correcto del campo en tu formulario

        if address:
            # Establecer el campo id_cliente de Address con el ID del cliente
            address.id_cliente = customer.customer_id
            address.save()

        return super().form_valid(form)
class EmployeeUpdateView(UpdateView):
    model = Employee
    form_class = EmployeeAddressForm
    template_name = 'address_form.html'
    success_url = reverse_lazy('employee:employee_list')  


class EmployeeListView(ListView):
    model = Employee
    template_name = 'employee_list.html'
    context_object_name = 'employee'


class EmployeeDeleteView(DeleteView):
    model = Employee
    success_url = reverse_lazy('employee:employee_list')


class MarkEntryView(CreateView):
    model = EntryRecord
    fields = []  # You can customize fields if necessary
    template_name = 'employee_lis.html'  # Replace 'your_template.html' with the desired template
    success_url = reverse_lazy('employee:employee_list')  # Replace 'Employees:list' with the appropriate success URL

    def form_valid(self, form):
        # Obtén el empleado actualmente autenticado
        employee = self.request.user


        # Check the entry
        if not employee.check_today_entry():
            # Create an entry record for the employee
            entry_record = form.save(commit=False)
            entry_record.employee = employee
            entry_record.save()

            # Check if the employee is late based on their schedule
            current_time = datetime.now().time()
            entry_schedule = EntrySchedule.objects.filter(employee=employee).first()

            if entry_schedule:
                if current_time > entry_schedule.entry_time:
                    # Calculate the number of minutes late
                    tardiness_minutes = (datetime.combine(datetime.today(), current_time) - datetime.combine(datetime.today(), entry_schedule.entry_time)).total_seconds() / 60
                    tardiness_minutes = round(tardiness_minutes)

                    # Create a discipline record for tardiness
                    discipline_reason = f"Late arrival by {tardiness_minutes} minutes"
                    discipline_date = datetime.now().date()
                    DisciplineRecord.objects.create(employee=employee, discipline_date=discipline_date, discipline_reason=discipline_reason)

        return super().form_valid(form)
    


class MarkExitView(UpdateView):
    model = EntryRecord
    fields = ['exit_date']  # You can customize fields if necessary
    template_name = 'employee_lis.html'  # Replace 'your_template.html' with the desired template
    success_url = reverse_lazy('employee:employee_list')  # Replace 'Employees:list' with the appropriate success URL

    def get_object(self, queryset=None):
        # Obtén el registro de entrada correspondiente al empleado actualmente autenticado
        employee = self.request.user
        return EntryRecord.objects.filter(employee=employee, exit_date__isnull=True).order_by('-entry_date').first()

    def form_valid(self, form):
        # Retrieve the EntryRecord object
        entry_record = form.save(commit=False)
        
        # Check if there's a matching entry record for the exit
        if entry_record.entry_date is None:
            form.add_error(None, "There is no matching entry record for this exit.")
            return self.form_invalid(form)

        # Mark the exit and save the record
        entry_record.exit_date = timezone.now()
        entry_record.save()

        # Check if the employee has an exit schedule defined
        employee = entry_record.employee
        exit_schedule = EntrySchedule.objects.filter(employee=employee).first()

        if exit_schedule and entry_record.exit_date.time() != exit_schedule.exit_time:
            # Calculate the number of minutes of deviation
            deviation_minutes = abs((entry_record.exit_date - timezone.now()).total_seconds() / 60)

            # Create a discipline record for deviation
            discipline_reason = f"Deviation from exit schedule by {deviation_minutes} minutes"
            discipline_date = timezone.now().date()
            DisciplineRecord.objects.create(employee=employee, discipline_date=discipline_date, discipline_reason=discipline_reason)

        return super().form_valid(form)