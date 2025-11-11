
from django.http import JsonResponse
from django.shortcuts import redirect, render

from django.contrib import messages   # ✅ correct import





def index(request):
    services = Service.objects.all()
    testimonials = Testimonial.objects.all()
    videos = VideoTestimonial.objects.all().order_by('-uploaded_at')
    banner = Banner.objects.filter(is_active=True).first()  # get active banner
    return render(request, 'app/index.html', {
        'services': services,
        'testimonials': testimonials,
        'videos': videos,
        'banner': banner,
    })

def contact_view(request):
    return render(request, 'app/contact.html')

from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Testimonial, VideoTestimonial

def testimonial_view(request):
    testimonials = Testimonial.objects.all().order_by('-id')
    videos = VideoTestimonial.objects.all().order_by('-uploaded_at')


    context = {
        'testimonials': testimonials,
        'videos': videos,
    }
    return render(request, 'app/testimonial.html', context)



def about_view(request):
    return render(request, 'app/about.html')

def Error_view(request):
    return render(request, 'app/404.html')              

def add_staff(request):
    return render(request, 'dash/add_staff.html')             

def base(request):
    return render(request, 'app/base.html')              
         


# app/views.py
from django.shortcuts import render, redirect
from .models import Staff,StaffSalary

def add_staff(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        role = request.POST.get("role")
        address = request.POST.get("address")
        photo = request.FILES.get("photo")

         # Handle active/inactive
        # is_active = True if request.POST.get("is_active") else False
        is_active = True 
        staff = Staff(
            name=name,
            phone=phone,
            role=role,
            address=address,
            photo=photo,
            is_active=is_active,
        )
        staff.save()   # ✅ Correct usage
        # messages.success(request, "✅ Data saved successfully!")
        return redirect("staff_list")  # redirect back to form page
        # return redirect("add_staff") 
    
    return render(request, "dash/add_staff.html")


from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Staff

def staff_list(request):
    query = request.GET.get("q", "")
    staff_qs = Staff.objects.all().order_by("-id")

    if query:
        staff_qs = staff_qs.filter(name__icontains=query)

    # Pagination — show 10 staff per page
    paginator = Paginator(staff_qs, 10)
    page_number = request.GET.get("page")
    staff_page = paginator.get_page(page_number)

    return render(request, "dash/staff_list.html", {
        "staff": staff_page,
        "query": query
    })



def staff_detail(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    return render(request, 'dash/staff_icard.html', {'staff': staff})


# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Staff, StaffSalary

def add_salary(request):
    if request.method == "POST":
        staff_id = request.POST.get("staff")
        staff = get_object_or_404(Staff, id=staff_id)

        month_date = request.POST.get("month_date")
        basic_salary = request.POST.get("basic_salary")
        allowance = request.POST.get("allowance", 0) or 0
        deduction = request.POST.get("deduction", 0) or 0
        net_salary = request.POST.get("net_salary")
        status = request.POST.get("status")

        StaffSalary.objects.create(
            staff=staff,
            month_date=month_date,
            basic_salary=basic_salary,
            allowance=allowance,
            deduction=deduction,
            net_salary=net_salary,
            status=status,
        )

        messages.success(request, "✅ Salary data saved successfully")
        return redirect("salary_list")  # Redirect to salary list after adding

    # 👇 make sure you are sending staff_members
    staff_members = Staff.objects.filter(is_active=True).order_by("name")
    return render(request, "dash/add_salary.html", {"staff_members": staff_members})



def staff_search(request):
    query = request.GET.get("q", "")
    results = []
    if query:
        staff_members = Staff.objects.filter(name__icontains=query)[:10]  # limit results
        results = [{"id": s.id, "name": s.name} for s in staff_members]
    return JsonResponse(results, safe=False)


from django.core.paginator import Paginator

def salary_list(request):
    query = request.GET.get("q", "")
    salaries_qs = StaffSalary.objects.select_related("staff").all().order_by("-month_date")

    if query:
        salaries_qs = salaries_qs.filter(staff__name__icontains=query)

    # Pagination - 10 records per page
    paginator = Paginator(salaries_qs, 10)
    page_number = request.GET.get("page")
    salaries_page = paginator.get_page(page_number)

    return render(request, "dash/salary_list.html", {
        "salaries": salaries_page,
        "query": query
    })



from django.shortcuts import render, redirect, get_object_or_404
from .models import StaffSalary, Staff
from decimal import Decimal

def edit_salary(request, id):
    salary = get_object_or_404(StaffSalary, id=id)  # Correct model name
    staff_members = Staff.objects.all()

    if request.method == "POST":
        staff_id = request.POST.get("staff")
        month_date = request.POST.get("month_date")
        basic_salary = request.POST.get("basic_salary")
        allowance = request.POST.get("allowance")
        deduction = request.POST.get("deduction")
        net_salary = request.POST.get("net_salary")
        status = request.POST.get("status")

        # update fields (convert numbers to Decimal)
        salary.staff_id = staff_id
        salary.month_date = month_date
        salary.basic_salary = Decimal(basic_salary) if basic_salary else 0
        salary.allowance = Decimal(allowance) if allowance else 0
        salary.deduction = Decimal(deduction) if deduction else 0
        salary.net_salary = Decimal(net_salary) if net_salary else (
            salary.basic_salary + salary.allowance - salary.deduction
        )
        salary.status = status
        salary.save()

        return redirect("salary_list")  # back to list

    return render(request, "dash/edit_salary.html", {
        "salary": salary,
        "staff_members": staff_members
    })


from django.shortcuts import render, get_object_or_404, redirect
from .models import Staff

def edit_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)

    if request.method == "POST":
        staff.name = request.POST.get("name")
        staff.phone = request.POST.get("phone")
        staff.role = request.POST.get("role")
        staff.address = request.POST.get("address")

        # Handle photo update only if a new one is uploaded
        if request.FILES.get("photo"):
            staff.photo = request.FILES.get("photo")

        staff.save()
        return redirect("staff_list")   # after update go back to list

    return render(request, "dash/edit_staff.html", {"staff": staff})



def delete_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    staff.delete()
    messages.success(request, "Staff deleted successfully ❌")
    return redirect("staff_list")


from django.shortcuts import render, redirect
from .models import Product

def add_product(request):
    if request.method == "POST":
        name = request.POST.get("name")
        rate = request.POST.get("rate")
        image = request.FILES.get("image")   # ✅ handle image

        if name and rate:
            Product.objects.create(name=name, rate=rate, image=image)
            return redirect("product_list")

    return render(request, "dash/add_product.html")


from django.core.paginator import Paginator

def product_list(request):
    query = request.GET.get("q", "")  # Get search text from input box
    products_qs = Product.objects.all().order_by("-id")

    if query:
        products_qs = products_qs.filter(name__icontains=query)  # Search by product name

    # Pagination — 10 records per page
    paginator = Paginator(products_qs, 10)
    page_number = request.GET.get("page")
    products_page = paginator.get_page(page_number)

    return render(request, "dash/product_list.html", {
        "products": products_page,
        "query": query
    })



# Update Product
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        name = request.POST.get("name")
        rate = request.POST.get("rate")
        image = request.FILES.get("image")

        product.name = name
        product.rate = rate

        if image:  # only update image if user uploads
            product.image = image

        product.save()
        return redirect("product_list")

    return render(request, "dash/edit_product.html", {"product": product})


# Delete Product
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect("product_list")

from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Q
from .models import Product, Bill, BillItem
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

def next_bill_no():
    last = Bill.objects.order_by('-id').first()
    next_id = last.id + 1 if last else 1
    return f"BILL-{next_id:04d}"

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from .models import Bill

def bill_list(request):
    q = request.GET.get('q', '')
    bills = Bill.objects.all().order_by('-id')

    # Apply search filter
    if q:
        bills = bills.filter(
            Q(customer_name__icontains=q) |
            Q(bill_number__icontains=q) |
            Q(contact_number__icontains=q)
        )

    # Apply pagination (10 per page)
    paginator = Paginator(bills, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dash/bill_list.html', {'page_obj': page_obj, 'query': q})



from decimal import Decimal
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from .models import Bill, BillItem, Product

@transaction.atomic
def create_bill(request):
    products = Product.objects.all()

    if request.method == 'POST':
        # --- Customer details ---
        customer_name = request.POST.get('customer_name') or ''
        contact_number = request.POST.get('contact_number') or ''
        address = request.POST.get('address') or ''
        bill_date = request.POST.get('bill_date') or timezone.now().date()
        event_date = request.POST.get('event_date') or None
        discount = Decimal(request.POST.get('discount') or '0')
        additional_charges = Decimal(request.POST.get('additional_charges') or '0')
        advance = Decimal(request.POST.get('advance') or '0')
        payment_method = request.POST.get('payment_method') or 'Cash'


        # --- Create & SAVE bill first ---
        bill = Bill (
            customer_name=customer_name,
            contact_number=contact_number,
            address=address,
            bill_date=bill_date,
            event_date=event_date,
            discount=discount,
            additional_charges=additional_charges,
            advance=advance,
            payment_method=payment_method,  # ✅ added
        )
        bill.save()   # ✅ explicitly save before using it in BillItem

        # --- Handle Bill Items ---
        product_ids = request.POST.getlist('product[]')
        descriptions = request.POST.getlist('description[]')
        quantities = request.POST.getlist('quantity[]')
        days_list = request.POST.getlist('days[]')
        rates = request.POST.getlist('rate[]')

        subtotal = Decimal('0.00')

        for i in range(len(product_ids)):
            pid = product_ids[i]
            if not pid:
                continue

            try:
                product = Product.objects.get(id=pid)
            except Product.DoesNotExist:
                continue

            qty = int(quantities[i] or 0)
            days = int(days_list[i] or 1)
            rate = Decimal(rates[i] or '0')
            desc = descriptions[i] if i < len(descriptions) else product.name

            amount = qty * rate * days
            subtotal += amount

            BillItem.objects.create(
                bill=bill,
                product=product,
                description=desc,
                quantity=qty,
                days=days,
                rate=rate,
                amount=amount
            )

        # --- Update totals and save again ---
        bill.subtotal = subtotal
        bill.grand_total = subtotal - discount + additional_charges
        bill.due_amount = bill.grand_total - advance
        bill.save()

        messages.success(request, f"Bill #{bill.bill_number} created successfully!")
        return redirect('bill_list')

    return render(request, 'dash/create_bill.html', {
        'products': products,
        'next_bill_no': next_bill_no()
    })



@transaction.atomic
def edit_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    products = Product.objects.all()
    items = bill.items.all().order_by('id')

    if request.method == 'POST':
        # update bill meta
        bill.customer_name = request.POST.get('customer_name') or ''
        bill.contact_number = request.POST.get('contact_number') or ''
        bill.address = request.POST.get('address') or ''
        bill.bill_date = request.POST.get('bill_date') or bill.bill_date
        bill.event_date = request.POST.get('event_date') or bill.event_date
        bill.discount = Decimal(request.POST.get('discount') or '0')
        bill.additional_charges = Decimal(request.POST.get('additional_charges') or '0')
        bill.advance = Decimal(request.POST.get('advance') or '0')

        # delete existing items and recreate from posted arrays
        bill.items.all().delete()

        product_ids = request.POST.getlist('product[]')
        descriptions = request.POST.getlist('description[]')
        quantities = request.POST.getlist('quantity[]')
        days_list = request.POST.getlist('days[]')
        rates = request.POST.getlist('rate[]')

        for i in range(len(product_ids)):
            pid = product_ids[i]
            if not pid:
                continue
            product = None
            try:
                product = Product.objects.get(id=pid)
            except Product.DoesNotExist:
                product = None
            qty = int(quantities[i] or 0)
            days = int(days_list[i] or 0)
            rate = Decimal(rates[i] or '0')
            desc = descriptions[i] if i < len(descriptions) else (product.name if product else '')
            BillItem.objects.create(
                bill=bill,
                product=product,
                description=desc,
                quantity=qty,
                days=days,
                rate=rate
            )

        bill.save()
        return redirect('bill_list')

    return render(request, 'dash/edit_bill.html', {
        'bill': bill,
        'products': products,
        'items': items
    })


# AJAX endpoint to retrieve product rate
@csrf_exempt
def get_product_rate(request):
    product_id = request.GET.get('product_id')
    try:
        p = Product.objects.get(id=product_id)
        return JsonResponse({'rate': float(p.rate)})
    except Product.DoesNotExist:
        return JsonResponse({'rate': 0.0})

#Bill Detail PDF View
from django.shortcuts import render, get_object_or_404
from .models import Bill
from django.utils import timezone

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Bill, BillItem

# 📄 Show Bill Details (HTML Invoice)
def bill_detail(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    items = bill.items.all()  # related_name from BillItem
    bank_detail = BankDetail.objects.last()  # assuming only one set of bank details
    return render(request, 'dash/bill_pdf.html', {
        'bill': bill,
        'items': items,
        'bank_detail': bank_detail,
    })


# 🗑️ Delete Bill + Related Items
def delete_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    if request.method == 'POST':
        bill.delete()
        return redirect('bill_list')
    return render(request, 'dash/delete_confirm.html', {'bill': bill})


# Income Dashboard View
from django.shortcuts import render
from django.db.models import Sum, F, FloatField, ExpressionWrapper
from .models import Bill


from django.core.paginator import Paginator
from django.db.models import Sum, F, FloatField, ExpressionWrapper

def income_dashboard(request):
    bills = Bill.objects.all()

    # Apply filters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    payment_method_filter = request.GET.get('payment_method', 'All')

    if start_date:
        bills = bills.filter(bill_date__gte=start_date)
    if end_date:
        bills = bills.filter(bill_date__lte=end_date)
    if payment_method_filter and payment_method_filter != 'All':
        bills = bills.filter(payment_method=payment_method_filter)

    # Annotate each bill with 'paid_amount'
    bills = bills.annotate(
        paid_amount=ExpressionWrapper(
            F('grand_total') - F('pending'),
            output_field=FloatField()
        )
    )

    # Pagination — Show 10 records per page
    paginator = Paginator(bills, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Summary calculations
    total_income = sum(b.paid_amount for b in bills)
    total_pending = sum(b.pending for b in bills)
    total_advance = sum(b.advance for b in bills)
    total_grand_total = sum(b.grand_total for b in bills)

    breakdown = bills.values('payment_method').annotate(amount=Sum('paid_amount')).order_by()

    context = {
        'page_obj': page_obj,  # Updated
        'bills': page_obj,     # For compatibility with your existing template
        'total_income': total_income,
        'total_pending': total_pending,
        'total_advance': total_advance,
        'total_grand_total': total_grand_total,
        'breakdown': breakdown,
        'start_date': start_date or '',
        'end_date': end_date or '',
        'payment_method_filter': payment_method_filter,
    }

    return render(request, 'dash/income.html', context)



import csv
from django.http import HttpResponse
from openpyxl import Workbook
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import csv
from django.http import HttpResponse
from openpyxl import Workbook
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.db.models import Sum, F, FloatField, ExpressionWrapper
from django.utils.dateparse import parse_date
from openpyxl import Workbook
from django.http import HttpResponse
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def export_income(request, file_type):
    # Apply same filters used in income_dashboard
    bills = Bill.objects.all()

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    payment_method = request.GET.get('payment_method')

    if start_date:
        bills = bills.filter(bill_date__gte=parse_date(start_date))
    if end_date:
        bills = bills.filter(bill_date__lte=parse_date(end_date))
    if payment_method and payment_method != "All":
        bills = bills.filter(payment_method=payment_method)

    # Annotate for calculations
    bills = bills.annotate(
        paid_amount=ExpressionWrapper(
            F('grand_total') - F('pending'),
            output_field=FloatField()
        )
    )

    # Summary Data
    total_income = sum(b.grand_total for b in bills)
    total_pending = sum(b.pending for b in bills)
    total_advance = sum(b.advance for b in bills)
    breakdown = bills.values('payment_method').annotate(amount=Sum('grand_total')).order_by()

    # === CSV Export ===
    if file_type == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="income_report.csv"'
        writer = csv.writer(response)
        writer.writerow(['Bill No', 'Customer', 'Bill Date', 'Event Date', 'Payment Method', 'Grand Total', 'Advance', 'Pending'])
        for bill in bills:
            writer.writerow([
                bill.bill_number,
                bill.customer_name,
                bill.bill_date.strftime("%d-%m-%Y") if bill.bill_date else "",
                bill.event_date.strftime("%d-%m-%Y") if bill.event_date else "",
                bill.payment_method,
                bill.grand_total,
                bill.advance,
                bill.pending
            ])
        return response

    # === Excel Export ===
    elif file_type == 'excel':
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="income_dashboard.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.title = "Income Summary"

        # Summary section
        ws.append(["Income Dashboard Summary"])
        ws.append([])
        ws.append(["Total Income", float(total_income)])
        ws.append(["Total Pending", float(total_pending)])
        ws.append(["Total Advance", float(total_advance)])
        ws.append([])
        ws.append(["Breakdown by Payment Type"])
        ws.append(["Payment Method", "Amount"])
        for b in breakdown:
            ws.append([b['payment_method'], float(b['amount'])])

        ws.append([])
        ws.append(["Filtered Bills"])
        ws.append(['Bill No', 'Customer', 'Bill Date', 'Event Date', 'Payment Method', 'Grand Total', 'Advance', 'Pending'])
        for bill in bills:
            ws.append([
                bill.bill_number,
                bill.customer_name,
                bill.bill_date.strftime("%d-%m-%Y") if bill.bill_date else "",
                bill.event_date.strftime("%d-%m-%Y") if bill.event_date else "",
                bill.payment_method,
                float(bill.grand_total),
                float(bill.advance),
                float(bill.pending)
            ])
        wb.save(response)
        return response

    # === PDF Export ===
    elif file_type == 'pdf':
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="income_report.pdf"'
        p = canvas.Canvas(response, pagesize=letter)
        width, height = letter
        y = height - 50
        p.setFont("Helvetica-Bold", 14)
        p.drawString(220, y, "Income Report")
        y -= 40
        p.setFont("Helvetica", 10)

        # Summary
        p.drawString(40, y, f"Total Income: ₹{total_income:.2f}")
        y -= 20
        p.drawString(40, y, f"Total Pending: ₹{total_pending:.2f}")
        y -= 20
        p.drawString(40, y, f"Total Advance: ₹{total_advance:.2f}")
        y -= 30

        # Breakdown
        p.drawString(40, y, "Breakdown by Payment Type:")
        y -= 20
        for b in breakdown:
            p.drawString(60, y, f"{b['payment_method']}: ₹{b['amount']:.2f}")
            y -= 20

        y -= 30
        p.setFont("Helvetica-Bold", 11)
        p.drawString(40, y, "Filtered Bill Details:")
        y -= 20
        p.setFont("Helvetica", 9)
        for bill in bills:
            p.drawString(
                40, y,
                f"{bill.bill_number} | {bill.customer_name} | {bill.payment_method} | ₹{bill.grand_total} | Adv: ₹{bill.advance} | Pend: ₹{bill.pending}"
            )
            y -= 15
            if y < 50:
                p.showPage()
                y = height - 50
        p.save()
        return response

    else:
        return HttpResponse("Invalid export type")


# Expense views (append to views.py)
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from django.db.models import Sum
from decimal import Decimal
from .models import Expense, ExpenseCategory, Staff, StaffSalary
from django.utils.dateparse import parse_date
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Expense, ExpenseCategory, Staff

def add_expense(request):
    categories = ExpenseCategory.objects.all()
    staff_members = Staff.objects.all()

    if request.method == "POST":
        category_id = request.POST.get('category')
        staff_id = request.POST.get('staff')
        amount = request.POST.get('amount')
        date_str = request.POST.get('date')  # get the string from form
        payment_mode = request.POST.get('payment_mode')
        description = request.POST.get('description')

        # Parse date safely; default to today if empty or invalid
        if date_str:
            try:
                date_obj = parse_date(date_str)
                if date_obj is None:
                    raise ValueError
            except:
                messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
                return redirect('add_expense')
        else:
            date_obj = datetime.date.today()

        # Handle new category inline
        if category_id == '__add_new__':
            new_category_name = request.POST.get('new_category_name')
            if not new_category_name:
                messages.error(request, "Please enter a name for the new category before submitting.")
                return redirect('add_expense')
            
            category, created = ExpenseCategory.objects.get_or_create(name=new_category_name)
        else:
            try:
                category = get_object_or_404(ExpenseCategory, id=int(category_id))
            except ValueError:
                messages.error(request, "Invalid category selected.")
                return redirect('add_expense')

        # Staff is optional
        staff = Staff.objects.filter(id=staff_id).first() if staff_id else None

        # Create expense
        Expense.objects.create(
            category=category,
            staff=staff,
            amount=amount,
            date=date_obj,  # use parsed/default date
            payment_mode=payment_mode,
            description=description
        )

        messages.success(request, "Expense added successfully!")
        return redirect('expense_dashboard')

    context = {
        "categories": categories,
        "staff_members": staff_members,
    }
    return render(request, "dash/expense_form.html", context)


from django.db.models import Sum
from django.utils.dateparse import parse_date
from decimal import Decimal
import datetime
from django.core.paginator import Paginator
from decimal import Decimal
from django.db.models import Sum
import datetime
from django.utils.dateparse import parse_date

def expense_dashboard(request):
    qs = Expense.objects.select_related('category', 'staff').all()

    # ---- Filters ----
    start_date = request.GET.get('start_date') or ''
    end_date = request.GET.get('end_date') or ''
    category_id = request.GET.get('category') or ''
    staff_id = request.GET.get('staff') or ''
    payment_method = request.GET.get('payment_method') or 'All'

    if start_date:
        try:
            sd = parse_date(start_date)
            qs = qs.filter(date__gte=sd)
        except:
            pass
    if end_date:
        try:
            ed = parse_date(end_date)
            qs = qs.filter(date__lte=ed)
        except:
            pass
    if category_id:
        qs = qs.filter(category_id=category_id)
    if staff_id:
        qs = qs.filter(staff_id=staff_id)
    if payment_method and payment_method != 'All':
        qs = qs.filter(payment_mode=payment_method)

    # ---- Summary ----
    total_expense = qs.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    total_staff_salary = StaffSalary.objects.aggregate(total=Sum('net_salary'))['total'] or Decimal('0.00')

    today = datetime.date.today()
    first_of_month = today.replace(day=1)
    month_qs = qs.filter(date__gte=first_of_month, date__lte=today)
    month_total = month_qs.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    cat_breakdown = qs.values('category__name').annotate(total=Sum('amount')).order_by('-total')[:10]
    payment_breakdown = qs.values('payment_mode').annotate(amount_sum=Sum('amount')).order_by('payment_mode')

    categories = ExpenseCategory.objects.all().order_by('name')
    staff_members = Staff.objects.filter(is_active=True).order_by('name')

    # ---- Pagination ----
    paginator = Paginator(qs, 10)  # Show 10 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    today_date = datetime.date.today()

    return render(request, 'dash/expense_dashboard.html', {
        'expenses': page_obj,  # Use page_obj in template
        'page_obj': page_obj,  # For pagination controls
        'total_expense': total_expense,
        'total_staff_salary': total_staff_salary,
        'month_total': month_total,
        'cat_breakdown': cat_breakdown,
        'categories': categories,
        'staff_members': staff_members,
        'payment_breakdown': payment_breakdown,
        'today_date': today_date,
        'filters': {
            'start_date': start_date,
            'end_date': end_date,
            'category_id': category_id,
            'staff_id': staff_id,
            'payment_method': payment_method,
        }
    })



# AJAX endpoint to get latest salary for selected staff (returns net_salary or 0)
def ajax_get_staff_salary(request):
    staff_id = request.GET.get('staff_id')
    if not staff_id:
        return JsonResponse({'success': False, 'salary': 0})
    try:
        staff = Staff.objects.get(id=int(staff_id))
    except Staff.DoesNotExist:
        return JsonResponse({'success': False, 'salary': 0})
    last_salary = StaffSalary.objects.filter(staff=staff).order_by('-month_date').first()
    if last_salary:
        return JsonResponse({'success': True, 'salary': float(last_salary.net_salary)})
    else:
        return JsonResponse({'success': True, 'salary': 0})


# AJAX to add new category quickly (called from form)
def ajax_add_category(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("POST required")
    name = (request.POST.get('name') or '').strip()
    if not name:
        return JsonResponse({'success': False, 'error': 'Empty name'})
    obj, created = ExpenseCategory.objects.get_or_create(name=name)
    return JsonResponse({'success': True, 'id': obj.id, 'name': obj.name})



from openpyxl import Workbook
from django.http import HttpResponse
from .models import Expense, ExpenseCategory, Staff
from django.db.models import Sum
from django.utils.dateparse import parse_date
import datetime
def export_expenses(request, file_type):
    if file_type != 'excel':
        return HttpResponse("Invalid export type")

    qs = Expense.objects.select_related('category', 'staff').all()

    # Apply filters from GET
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    category_id = request.GET.get('category')
    staff_id = request.GET.get('staff')
    payment_method = request.GET.get('payment_method')

    if start_date:
        qs = qs.filter(date__gte=parse_date(start_date))
    if end_date:
        qs = qs.filter(date__lte=parse_date(end_date))
    if category_id:
        qs = qs.filter(category_id=category_id)
    if staff_id:
        qs = qs.filter(staff_id=staff_id)
    if payment_method:
        qs = qs.filter(payment_mode=payment_method)

    # 🧩 Bonus: Include all data when no records found
    if not qs.exists():
        qs = Expense.objects.all()

    # Create workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Expense Report"

    # Header
    ws.append(['Date', 'Category', 'Staff', 'Amount', 'Payment Mode', 'Description'])

    # Data rows
    for e in qs:
        ws.append([
            e.date.strftime("%d-%m-%Y") if e.date else "",
            e.category.name if e.category else "",
            e.staff.name if e.staff else "",
            float(e.amount),
            e.payment_mode,
            e.description or ""
        ])

    # Prepare response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=expense_report.xlsx'
    wb.save(response)
    return response


from urllib.parse import quote
from django.shortcuts import redirect, get_object_or_404
from .models import Bill

def send_reminder(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)

    message = (
        f"🌸 Dear {bill.customer_name},\n\n"
        f"Thank you for choosing * New Mahavir Tent & Event Management* 💐\n\n"
        f"Your total bill amount is ₹{bill.grand_total}, "
        f"advance paid ₹{bill.advance}, and pending ₹{bill.pending}.\n\n"
        f"Kindly clear the pending amount at your earliest convenience.\n\n"
        f"We truly appreciate your trust in us and look forward to serving you again!\n\n"
        f"– New Mahavir Tent & Event Management Jamner. 🎪"
    )

    # ✅ Properly encode full message for WhatsApp
    encoded_message = quote(message)
    whatsapp_url = f"https://wa.me/91{bill.contact_number}?text={encoded_message}"

    return redirect(whatsapp_url)





# DASHBOARD VIEW
from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone
from datetime import date, timedelta
from .models import Bill, Expense, Staff, StaffSalary
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


@never_cache
@login_required
def dashboard(request):
    today = date.today()
    current_month = today.month
    current_year = today.year

    # ---- SUMMARY CARDS ----
    total_income_today = Bill.objects.filter(bill_date=today).aggregate(Sum('grand_total'))['grand_total__sum'] or 0
    total_expense_today = Expense.objects.filter(date=today).aggregate(Sum('amount'))['amount__sum'] or 0
    total_pending = Bill.objects.aggregate(Sum('pending'))['pending__sum'] or 0
    profit_today = total_income_today - total_expense_today

    # Upcoming event bookings
    upcoming_events = Bill.objects.filter(event_date__gte=today).order_by('event_date')[:5]

    # Stat cards
    total_income = Bill.objects.aggregate(Sum('grand_total'))['grand_total__sum'] or 0
    total_events = Bill.objects.filter(event_date__gte=today).count()
    new_clients = Bill.objects.values('customer_name').distinct().count()
    total_expense = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0

    # ---- MONTHLY INCOME & EXPENSES ----
    monthly_income = (
        Bill.objects.filter(bill_date__year=current_year)
        .values_list('bill_date__month')
        .annotate(total=Sum('grand_total'))
        .order_by('bill_date__month')
    )

    monthly_expense = (
        Expense.objects.filter(date__year=current_year)
        .values_list('date__month')
        .annotate(total=Sum('amount'))
        .order_by('date__month')
    )

    income_data = [0]*12
    expense_data = [0]*12

    for month, total in monthly_income:
        income_data[month-1] = float(total)
    for month, total in monthly_expense:
        expense_data[month-1] = float(total)

    # Payment method distribution
    payment_modes = (
        Bill.objects.values('payment_method')
        .annotate(total=Sum('grand_total'))
        .order_by('payment_method')
    )

    # Line graph (last 6 months)
    last_6_months = []
    income_last_6 = []
    for i in range(5, -1, -1):
        month = (today.replace(day=1) - timedelta(days=30*i))
        month_total = Bill.objects.filter(
            bill_date__month=month.month,
            bill_date__year=month.year
        ).aggregate(Sum('grand_total'))['grand_total__sum'] or 0
        last_6_months.append(month.strftime('%b'))
        income_last_6.append(float(month_total))

    # Event calendar data
    calendar_events = [
        {
            'title': f"{bill.customer_name} - ₹{bill.grand_total}",
            'start': bill.event_date.strftime('%Y-%m-%d'),
            'color': '#0d6efd'
        }
        for bill in upcoming_events
    ]

    context = {
        # summary
        "total_income_today": total_income_today,
        "total_expense_today": total_expense_today,
        "total_pending": total_pending,
        "profit_today": profit_today,
        "total_expense": total_expense,

        # charts
        "income_data": income_data,
        "expense_data": expense_data,
        "payment_modes": payment_modes,
        "last_6_months": last_6_months,
        "income_last_6": income_last_6,

        # calendar
        "calendar_events": calendar_events,

        # other stats
        'upcoming_events': upcoming_events,
        'total_income': total_income,
        'total_events': total_events,
        'new_clients': new_clients,
    }

    # --- ROLE-BASED DASHBOARD ---
    if request.user.role == 'admin':
        return render(request, 'dash/dashboard.html', context)
    elif request.user.role == 'manager':
        return render(request, 'dash/manager_dashboard.html', context)
    else:
        messages.error(request, "Unknown role")
        return redirect('login')

# Authentication Views

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'admin':
                return redirect('dashboard')  # admin dashboard
            else:
                return redirect('dashboard')  # manager dashboard (can customize)
        else:
            messages.error(request, "Invalid email or password")
    return render(request, 'auth/login.html')
    
def logout_view(request):
    logout(request)
    return redirect('login')



# Prfile View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

@never_cache
@login_required
def profile(request):
    user = request.user  # ✅ make available everywhere

    if request.method == "POST":
        name = request.POST.get('name')
        password = request.POST.get('password')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        profile_image = request.FILES.get('profile_image')

        # ✅ Update only if provided
        if name:
            user.first_name = name  # or `user.username = name` depending on your CustomUser fields

        if email:  
            user.email = email  # update only if email entered, prevents NULL error

        if contact:
            user.contact = contact

        if profile_image:
            user.profile_image = profile_image

        if password:
            user.set_password(password)

        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('profile')

    return render(request, 'dash/profile.html', {'user': user})


from django.contrib.auth import get_user_model

User = get_user_model()


# app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from .models import CustomUser

@never_cache
@login_required
def register_user(request):
    users = CustomUser.objects.all().order_by('-id')

    # --- ADD USER ---
    if request.method == "POST" and "add_user" in request.POST:
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")
        contact = request.POST.get("contact")
        profile_image = request.FILES.get("profile_image")

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "A user with this email already exists.")
            return redirect('register_user')

        CustomUser.objects.create(
            name=name,
            email=email,
            role=role,
            contact=contact,
            profile_image=profile_image,
            password=make_password(password)
        )
        messages.success(request, f"User '{name}' registered successfully.")
        return redirect('register_user')

    # --- DELETE USER ---
    if request.method == "POST" and "delete_user" in request.POST:
        user_id = request.POST.get("delete_user")
        user = get_object_or_404(CustomUser, id=user_id)
        user.delete()
        messages.success(request, "User deleted successfully.")
        return redirect('register_user')

    # --- EDIT USER ---
    if request.method == "POST" and "edit_user" in request.POST:
        user_id = request.POST.get("edit_user")
        user = get_object_or_404(CustomUser, id=user_id)
        user.name = request.POST.get("edit_name")
        user.role = request.POST.get("edit_role")
        user.contact = request.POST.get("edit_contact")
        profile_image = request.FILES.get("edit_profile_image")
        if profile_image:
            user.profile_image = profile_image
        user.save()
        messages.success(request, "User updated successfully.")
        return redirect('register_user')

    return render(request, "dash/register_user.html", {"users": users})


@never_cache
@login_required
def manager_dashboard(request):
    today = date.today()
    bills = Bill.objects.filter(created_by=request.user)
    total_income = bills.aggregate(Sum('grand_total'))['grand_total__sum'] or 0

    context = {
        "total_income": total_income,
        "bills": bills,
        "today": today
    }
    return render(request, 'dash/manager_dashboard.html', context)


# Send Password Reset Email
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives  # ✅ changed
from django.utils.html import strip_tags

User = get_user_model()

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            # Create token + uid
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Render HTML message
            mail_subject = "Reset Your Mahavir Tent Account Password"
            html_message = render_to_string('auth/password_reset_email.html', {
                'user': user,
                'domain': request.get_host(),
                'uid': uid,
                'token': token,
                'protocol': 'https' if request.is_secure() else 'http',
            })

            # Convert HTML → plain text fallback
            text_message = strip_tags(html_message)

            # Send multipart email (HTML + text)
            email_msg = EmailMultiAlternatives(
                mail_subject,
                text_message,  # plain text fallback
                to=[email]
            )
            email_msg.attach_alternative(html_message, "text/html")  # ✅ HTML version
            email_msg.send()

            messages.success(request, "✅ Password reset email has been sent!")
            return redirect('login')
        else:
            messages.error(request, "❌ No account found with this email.")
    
    return render(request, 'auth/forgot_password.html')




from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect

User = get_user_model()

def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            if password1 and password2 and password1 == password2:
                user.set_password(password1)
                user.save()
                messages.success(request, "✅ Your password has been reset successfully.")
                return redirect('login')
            else:
                messages.error(request, "❌ Passwords do not match. Please try again.")

        return render(request, 'auth/reset_password.html', {'validlink': True})

    else:
        messages.error(request, "⚠️ The reset link is invalid or has expired.")
        return render(request, 'auth/reset_password.html', {'validlink': False})



@login_required
def manage_website(request):
    return render(request, 'dash/manage_website.html')


# gallery/views.py
from django.shortcuts import render
from .models import GalleryImage, GalleryCategory

def gallery_view(request):
    categories = {}
    all_categories = GalleryCategory.objects.all()
    for cat in all_categories:
        categories[cat.name] = GalleryImage.objects.filter(category=cat).order_by('-created_at')

    return render(request, 'app/gallery.html', {'categories': categories})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import GalleryImage, GalleryCategory

@login_required
def gallery_list(request):
    if request.method == "POST":
        # Add new category
        if "add_category" in request.POST:
            name = request.POST.get("category_name")
            if name:
                GalleryCategory.objects.create(name=name)
                messages.success(request, "Category added successfully.")
            else:
                messages.error(request, "Please enter a category name.")
            return redirect("gallery_list")

        # Add new gallery image
        elif "add_gallery" in request.POST:
            category_id = request.POST.get("category")
            place = request.POST.get("place")
            event_date = request.POST.get("event_date")
            image = request.FILES.get("image")

            if category_id and place and event_date and image:
                category = get_object_or_404(GalleryCategory, id=category_id)
                GalleryImage.objects.create(
                    category=category,
                    place=place,
                    event_date=event_date,
                    image=image
                )
                messages.success(request, "Gallery image added successfully.")
            else:
                messages.error(request, "Please fill all fields.")
            return redirect("gallery_list")

        # Delete gallery image
        elif "delete_gallery" in request.POST:
            gallery_id = request.POST.get("delete_gallery")
            gallery = get_object_or_404(GalleryImage, id=gallery_id)
            gallery.delete()
            messages.success(request, "Gallery image deleted successfully.")
            return redirect("gallery_list")

        # Delete category
        elif "delete_category" in request.POST:
            cat_id = request.POST.get("delete_category")
            category = get_object_or_404(GalleryCategory, id=cat_id)
            category.delete()
            messages.success(request, "Category deleted successfully.")
            return redirect("gallery_list")

    galleries = GalleryImage.objects.select_related("category").order_by("-created_at")
    categories = GalleryCategory.objects.all().order_by("name")

    paginator = Paginator(galleries, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "dash/gallery_list.html", {
        "galleries": page_obj,
        "page_obj": page_obj,
        "categories": categories,
    })




from .models import Service

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Service

@login_required
def service_list(request):
    if request.method == "POST":
        # Add Service
        if "add_service" in request.POST:
            title = request.POST.get("title")
            image = request.FILES.get("image")

            if title:
                Service.objects.create(title=title, image=image)
                messages.success(request, "Service added successfully.")
                return redirect("service_list")
            else:
                messages.error(request, "Please fill in the title field.")

        # Delete Service
        elif "delete_service" in request.POST:
            service_id = request.POST.get("delete_service")
            service = get_object_or_404(Service, id=service_id)
            service.delete()
            messages.success(request, "Service deleted successfully.")
            return redirect("service_list")

        # Edit Service
        elif "edit_service" in request.POST:
            service_id = request.POST.get("service_id")
            title = request.POST.get("title")     
            image = request.FILES.get("image")
            service = get_object_or_404(Service, id=service_id)
            service.title = title
            if image:
                service.image = image
            service.save()
            messages.success(request, "Service updated successfully.")
            return redirect("service_list")

    # --- Fetch services with pagination ---
    services_qs = Service.objects.all().order_by("title")
    paginator = Paginator(services_qs, 6)  # 6 records per page
    page_number = request.GET.get("page")
    services_page = paginator.get_page(page_number)

    return render(request, "dash/service_list.html", {
        "services": services_page,
        "page_obj": services_page
    })

from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Testimonial

@login_required
def testimonial_list(request):
    if request.method == "POST":
        # Add testimonial
        if "add_testimonial" in request.POST:
            name = request.POST.get("client_name")
            address = request.POST.get("client_address")
            feedback = request.POST.get("feedback")
            image = request.FILES.get("image")

            if name and feedback:
                Testimonial.objects.create(
                    client_name=name,
                    client_address=address,
                    feedback=feedback,
                    image=image
                )
                messages.success(request, "Testimonial added successfully.")
                return redirect("testimonial_list")
            else:
                messages.error(request, "Please fill in all required fields.")

        # Delete testimonial
        elif "delete_testimonial" in request.POST:
            testimonial_id = request.POST.get("delete_testimonial")
            testimonial = get_object_or_404(Testimonial, id=testimonial_id)
            testimonial.delete()
            messages.success(request, "Testimonial deleted successfully.")
            return redirect("testimonial_list")

        # Edit testimonial
        elif "edit_testimonial" in request.POST:
            testimonial_id = request.POST.get("testimonial_id")
            name = request.POST.get("client_name")
            address = request.POST.get("client_address")
            feedback = request.POST.get("feedback")
            image = request.FILES.get("image")
            testimonial = get_object_or_404(Testimonial, id=testimonial_id)
            testimonial.client_name = name
            testimonial.client_address = address
            testimonial.feedback = feedback
            if image:
                testimonial.image = image
            testimonial.save()
            messages.success(request, "Testimonial updated successfully.")
            return redirect("testimonial_list")

    # --- Fetch testimonials with pagination ---
    testimonials_qs = Testimonial.objects.all().order_by("-id")
    paginator = Paginator(testimonials_qs, 3)  # 6 testimonials per page
    page_number = request.GET.get("page")
    testimonials_page = paginator.get_page(page_number)

    return render(request, "dash/testimonial_list.html", {
        "testimonials": testimonials_page,
        "page_obj": testimonials_page,
    })


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import VideoTestimonial

@login_required
def video_testimonial_list(request):
    if request.method == "POST":
        # Add video
        if "add_video_testimonial" in request.POST:
            title = request.POST.get("title")
            video = request.FILES.get("video")

            if video:
                VideoTestimonial.objects.create(title=title, video_file=video)
                messages.success(request, "Video testimonial added successfully.")
            else:
                messages.error(request, "Please upload a valid video.")
            return redirect("video_testimonial_list")

        # Edit video title
        elif "edit_video_testimonial" in request.POST:
            vid_id = request.POST.get("vid_id")
            title = request.POST.get("title")
            video = get_object_or_404(VideoTestimonial, id=vid_id)
            video.title = title
            video.save()
            messages.success(request, "Video testimonial updated successfully.")
            return redirect("video_testimonial_list")

        # Delete video
        elif "delete_video_testimonial" in request.POST:
            vid_id = request.POST.get("delete_video_testimonial")
            video = get_object_or_404(VideoTestimonial, id=vid_id)
            video.delete()
            messages.success(request, "Video testimonial deleted.")
            return redirect("video_testimonial_list")

    videos = VideoTestimonial.objects.all().order_by('-uploaded_at')
    paginator = Paginator(videos, 12)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    return render(request, "dash/video_testimonial_list.html", {"page_obj": page_obj })





from .models import Banner
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Banner

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Banner

def manage_banner(request):
    banner = Banner.objects.first()  # get the existing one

    # Handle upload/update
    if request.method == "POST":
        title = request.POST.get('title')
        video = request.FILES.get('video')
        image = request.FILES.get('image')

        if banner:
            banner.title = title
            if video:
                banner.video = video
            if image:
                banner.image = image
            banner.is_active = True
            banner.save()
            messages.success(request, "Banner updated successfully!")
        else:
            Banner.objects.create(title=title, video=video, image=image, is_active=True)
            messages.success(request, "Banner added successfully!")

        return redirect('manage_banner')

    # Handle delete
    if request.GET.get("delete"):
        banner = get_object_or_404(Banner, id=request.GET.get("delete"))
        banner.delete()
        messages.success(request, "Banner deleted successfully!")
        return redirect('manage_banner')

    return render(request, 'dash/banner_edit.html', {"banner": banner})




from django.core.paginator import Paginator
from django.shortcuts import render
from .models import EventVideo

def events_page(request):
    videos_list = EventVideo.objects.all().order_by('-event_date', '-id')
    paginator = Paginator(videos_list, 9)  # 9 videos per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'app/events.html', {
        'event_videos': page_obj,  # ✅ match template variable
        'page_obj': page_obj,
    })



# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import EventVideo
from django.contrib import messages

# List & Add Event Videos
import re
from django.shortcuts import render, redirect
from .models import EventVideo

import re
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import EventVideo

def manage_event_videos(request): 
    if request.method == "POST":
        event_name = request.POST['event_name']
        place = request.POST['place']
        event_date = request.POST['event_date']
        youtube_url = request.POST['youtube_url']

        # (Optional) Validate YouTube link pattern
        pattern = r'(?:youtu\.be/|youtube\.com/(?:watch\?v=|embed/|v/))([A-Za-z0-9_-]{11})'
        match = re.search(pattern, youtube_url)
        if not match:
            # If invalid URL, you can show an error or skip saving
            return redirect('manage_event_videos')

        # ✅ Only save the YouTube URL — NOT the ID
        EventVideo.objects.create(
            event_name=event_name,
            place=place,
            event_date=event_date,
            youtube_url=youtube_url
        )

        return redirect('manage_event_videos')

    # ✅ Pagination: 6 per page
    videos_qs = EventVideo.objects.all().order_by('-event_date', '-id')
    paginator = Paginator(videos_qs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dash/manage_event_videos.html', {
        'videos': page_obj,
        'page_obj': page_obj
    })

# Delete Event Video
def delete_event_video(request, video_id):
    video = get_object_or_404(EventVideo, id=video_id)
    video.delete()
    messages.success(request, "Event video deleted")
    return redirect('manage_event_videos')


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage

def contact_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        subject = request.POST.get('subject')
        message_text = request.POST.get('message')

        # Save the message to DB
        ContactMessage.objects.create(
            name=name,
            email=email,
            mobile=mobile,
            address=address,
            subject=subject,
            message=message_text
        )

        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact')

    return render(request, 'app/contact.html')

from django.shortcuts import render
from .models import ContactMessage

def contact_messages_view(request):
    messages_list = ContactMessage.objects.all().order_by('-created_at')

     # Apply pagination (20 per page)
    paginator = Paginator(messages_list, 10)  # 10 messages per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dash/contact_msg.html', {'messages_list': messages_list , 'page_obj': page_obj})

from django.shortcuts import get_object_or_404
from django.contrib import messages

def delete_contact_message(request, pk):
    msg = get_object_or_404(ContactMessage, id=pk)
    msg.delete()
    messages.success(request, "Message deleted successfully!")
    return redirect('contact_messages')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BankDetail

@login_required
def bank_detail_update(request):
    # There will be only one bank detail record
    bank_detail, created = BankDetail.objects.get_or_create(id=1)

    if request.method == "POST":
        # Get data from request.POST
        account_name = request.POST.get("account_name")
        account_number = request.POST.get("account_number")
        ifsc = request.POST.get("ifsc")
        branch = request.POST.get("branch")

        # Get QR code file if uploaded
        upi_qr = request.FILES.get("upi_qr")

        # Update model
        bank_detail.account_name = account_name
        bank_detail.account_number = account_number
        bank_detail.ifsc = ifsc
        bank_detail.branch = branch
        if upi_qr:
            bank_detail.upi_qr = upi_qr

        bank_detail.save()
        messages.success(request, "Bank details updated successfully.")
        return redirect("bank_detail_update")

    return render(request, "dash/bank_detail_update.html", {"bank_detail": bank_detail})
