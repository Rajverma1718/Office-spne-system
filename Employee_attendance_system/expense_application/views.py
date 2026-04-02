from django.shortcuts import render

# Create your views here.
def expense_home(request):
    return render(request, 'expense_application/expense_home.html')

def add_expense(request):
    return render(request, 'expense_application/add_expense.html')

def add_voucher(request):
    return render(request, 'expense_application/add_voucher.html')