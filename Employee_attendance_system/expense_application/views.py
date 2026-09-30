from django.shortcuts import render, redirect, get_object_or_404
from .forms import ExpenseForm
from .models import Expense
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from datetime import datetime
from django.contrib.auth.models import User   
from django.contrib.auth.decorators import login_required  


# HOME
def expense_home(request):
    return render(request, 'expense_application/expense_home.html')


#  ADD EXPENSE
@login_required   
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES)

        if form.is_valid():
            expense = form.save(commit=False)

            #  ADD (Swipe jaisa)
            expense.user = request.user
            expense.manager = User.objects.filter(username='manager1').first()

            #  FIX (lowercase status)
            expense.status = 'pending'

            #  SAFE CALCULATION (None handle)
            amount = expense.amount or 0
            rate = expense.conversion_rate or 1
            expense.final_amount = expense.amount

            expense.save()

            return redirect('add_voucher')

        return render(request, 'expense_application/add_expense.html', {
            'form': form
        })

    else:
        form = ExpenseForm()

    return render(request, 'expense_application/add_expense.html', {'form': form})


#  ADD VOUCHER
@login_required   
def add_voucher(request):
    expenses = Expense.objects.none()
    error = None

    if request.method == 'POST':

        #  STEP 1: Selected expenses
        selected_ids = request.POST.getlist('selected_expenses')

        if selected_ids:
            request.session['selected_expenses'] = selected_ids
            request.session.modified = True

            return redirect('recent_expenses')

        # STEP 2: Filters
        claim_type = request.POST.get('claim_type')
        travel_type = request.POST.get('travel_type')
        city = request.POST.get('city')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        if all([claim_type, travel_type, city, from_date, to_date]):
            try:
                from_date = datetime.strptime(from_date, "%Y-%m-%d")
                to_date = datetime.strptime(to_date, "%Y-%m-%d")

                #  ADD user filter (important)
                expenses = Expense.objects.filter(
                    user=request.user,
                    claim_type=claim_type,
                    travel_type=travel_type,
                    city=city,
                    date__range=[from_date, to_date]
                ).order_by('-id')

            except ValueError:
                error = "❌ Invalid date format"

        else:
            error = "⚠️ Please fill all fields before searching"

    return render(request, 'expense_application/add_voucher.html', {
        'expenses': expenses,
        'error': error
    })


#  RECENT EXPENSES (PENDING ONLY)
from collections import defaultdict

@login_required
def recent_expenses(request):
    selected_ids = request.session.get('selected_expenses', [])

    # 🔥 FIX: fallback logic
    if selected_ids:
        expenses = Expense.objects.filter(
            id__in=selected_ids,
            user=request.user,
            status='pending'
        ).order_by('-date')
    else:
        #  SHOW ALL PENDING (important)
        expenses = Expense.objects.filter(
            user=request.user,
            status='pending'
        ).order_by('-date')

    grouped = defaultdict(list)

    for exp in expenses:
        month = exp.date.replace(day=1)
        grouped[month].append(exp)

    monthly_data = []

    for month, items in grouped.items():
        monthly_data.append({
            'month': month,
            'expenses': items,
            'total_amount': sum(e.amount for e in items),
            'total_final': sum(e.final_amount for e in items),
        })

    monthly_data = sorted(monthly_data, key=lambda x: x['month'], reverse=True)

    return render(request, 'expense_application/recent_expenses.html', {
        'monthly_data': monthly_data
    })

from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from expense_application.models import Expense

@login_required
def approve_expenses(request):

    expenses = Expense.objects.filter(
        user=request.user,
        status__iexact='approved'
    ).order_by('-date')

    grouped = defaultdict(list)

    for exp in expenses:
        key = exp.date.strftime("%Y-%m")
        grouped[key].append(exp)

    data = []

    for key in sorted(grouped.keys(), reverse=True):
        items = grouped[key]
        total = sum(e.amount for e in items)

        data.append({
            "month": items[0].date,
            "expenses": items,
            "total": total
        })

    return render(request, 'expense_application/approve_expenses.html', {
        'data': data
    })
from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from expense_application.models import Expense

@login_required
def reject_expenses(request):

    expenses = Expense.objects.filter(
        user=request.user,
        status__iexact='rejected'
    ).order_by('-date')

    grouped = defaultdict(list)

    for exp in expenses:
        key = exp.date.strftime("%Y-%m")
        grouped[key].append(exp)

    data = []

    for key in sorted(grouped.keys(), reverse=True):
        items = grouped[key]
        total = sum(e.amount for e in items)

        data.append({
            "month": items[0].date,
            "expenses": items,
            "total": total
        })

    return render(request, 'expense_application/reject_expenses.html', {
        'data': data
    })
#  MONTH DETAIL (IMPORTANT)
@login_required
def monthly_detail(request, year, month, status):

    expenses = Expense.objects.filter(
        user=request.user,
        status=status,  
        date__year=year,
        date__month=month
    ).order_by('-date')

    totals = expenses.aggregate(
        total_amount=Sum('amount')
    )

    month_name = datetime(year, month, 1).strftime('%B %Y')

    return render(request, 'expense_application/monthly_detail.html', {
        'expenses': expenses,
        'total_amount': totals['total_amount'] or 0,
        'month_name': month_name,
        'status': status
    })

