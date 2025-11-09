
import datetime
from time import timezone
from django.db import models
# ------------------------------------------------------------------
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, role='manager', **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, role='admin', **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
    ]
    

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='manager')
    contact = models.CharField(max_length=15, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
# ------------------------------------------------------------------

class Service(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='services/')

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    client_address = models.CharField(max_length=255)
    feedback = models.TextField()
    image = models.ImageField(upload_to='testimonials/')

    def __str__(self):
        return self.client_name

    
class Banner(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    video = models.FileField(upload_to='banners/videos/', blank=True, null=True)
    image = models.ImageField(upload_to='banners/images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title or "Homepage Banner"
    
    
from django.db import models

class GalleryCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Gallery Categories"

    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE)
    place = models.CharField(max_length=100)
    event_date = models.DateField()
    image = models.ImageField(upload_to='gallery/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.place} ({self.event_date})"

# models.py
from django.db import models

class EventVideo(models.Model):
    event_name = models.CharField(max_length=200)
    place = models.CharField(max_length=200)
    event_date = models.DateField()
    youtube_url = models.URLField(help_text="Paste full YouTube link, e.g., https://youtu.be/xyz")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_name} - {self.place}"

    @property
    def youtube_id(self):
        """
        Extract YouTube ID from URL for embedding
        """
        import re
        # Handles youtu.be/xyz and youtube.com/watch?v=xyz
        pattern = r'(?:v=|youtu\.be/)([a-zA-Z0-9_-]+)'
        match = re.search(pattern, self.youtube_url)
        if match:
            return match.group(1)
        return None


from django.db import models



class Staff(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    role = models.CharField(max_length=100)
    address = models.TextField()
    photo = models.ImageField(upload_to="staff_photos/", blank=True, null=True)
    joining_date = models.DateField(auto_now_add=True)  # auto adds on creation
    is_active = models.BooleanField(default=True)       # active/inactive staff
    def __str__(self):
        return self.name
    
class StaffSalary(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    month_date = models.DateField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10,
        choices=[("Paid", "Paid"), ("Unpaid", "Unpaid")],
        default="Unpaid"
    )

    def __str__(self):
        return f"{self.staff.name} - {self.month_date}"




from decimal import Decimal
from django.db import models
from django.utils import timezone
from django.db.models import Sum

class Product(models.Model):
    name = models.CharField(max_length=200)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.ImageField(upload_to="product_images/", blank=True, null=True)
    
    def __str__(self):
        return self.name


PAYMENT_METHOD_CHOICES = [
    ('Cash', 'Cash'),
    ('UPI', 'UPI'),
    ('Card', 'Card'),
]

from django.db import models
from django.db.models import Sum
from django.utils import timezone
from decimal import Decimal
from num2words import num2words


class Bill(models.Model):
    bill_number = models.CharField(max_length=20, unique=True, blank=True)

    # customer details
    customer_name = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    bill_date = models.DateField(default=timezone.now)
    event_date = models.DateField(blank=True, null=True)

    # money fields
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    additional_charges = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    advance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='Cash')  # 🆕 Added field
    grand_total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    pending = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    notes = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Generate bill number if not set
        if not self.bill_number:
            last = Bill.objects.order_by('-id').first()
            next_id = (last.id + 1) if last else 1
            self.bill_number = f"BILL-{next_id:04d}"

        # ✅ Only calculate totals if Bill has been saved before (has ID)
        if self.pk:
            subtotal = BillItem.objects.filter(bill=self).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
            self.subtotal = subtotal
            self.grand_total = (self.subtotal - (self.discount or Decimal('0.00')) + (self.additional_charges or Decimal('0.00')))
            self.pending = self.grand_total - (self.advance or Decimal('0.00'))

        super().save(*args, **kwargs)

    def total_in_words(self):
        return f"Rupees {num2words(int(self.grand_total))} only"

    def __str__(self):
        return self.bill_number


class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=255, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    days = models.PositiveIntegerField(default=1)
    rate = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    def save(self, *args, **kwargs):
        # auto-calculate rate
        if self.product and (not self.rate or self.rate == Decimal('0.00')):
            self.rate = self.product.rate

        # compute amount
        self.amount = Decimal(self.quantity) * Decimal(self.days) * Decimal(self.rate)
        super().save(*args, **kwargs)

        # update parent bill totals
        if self.bill_id:  # ✅ make sure parent bill exists
            subtotal = BillItem.objects.filter(bill=self.bill).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
            self.bill.subtotal = subtotal
            self.bill.grand_total = self.bill.subtotal - self.bill.discount + self.bill.additional_charges
            self.bill.pending = self.bill.grand_total - self.bill.advance
            self.bill.save()

    def __str__(self):
        return self.description or (self.product.name if self.product else "Item")


# Expenses models (append to your existing models.py)
from django.db import models
from decimal import Decimal
from django.utils import timezone

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name

PAYMENT_MODE_CHOICES = [
    ('Cash', 'Cash'),
    ('UPI', 'UPI'),
    ('Card', 'Card'),
    ('Bank', 'Bank Transfer'),
]

class Expense(models.Model):
    category = models.ForeignKey(ExpenseCategory, on_delete=models.SET_NULL, null=True, blank=True)
    staff = models.ForeignKey('Staff', on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    date = models.DateField(default=datetime.date.today)
    payment_mode = models.CharField(max_length=30, choices=PAYMENT_MODE_CHOICES, default='Cash')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        cat = self.category.name if self.category else "Uncategorized"
        return f"{cat} - ₹{self.amount} on {self.date}"


from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    address = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


from django.db import models

class BankDetail(models.Model):
    account_name = models.CharField(max_length=255, default="New Mahavir Tent House")
    account_number = models.CharField(max_length=50)
    ifsc = models.CharField(max_length=20)
    branch = models.CharField(max_length=255)
    upi_qr = models.ImageField(upload_to="bank_qr/", null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.account_name} ({self.account_number})"

import os
from django.db import models
from moviepy import VideoFileClip
from django.core.files import File
from tempfile import NamedTemporaryFile


class VideoTestimonial(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='testimonials_videos/')
    thumbnail = models.ImageField(upload_to='testimonials_thumbs/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.video_file and not self.thumbnail:
            self.generate_thumbnail()

    def generate_thumbnail(self):
        """Automatically create thumbnail from video."""
        try:
            clip = VideoFileClip(self.video_file.path)
            frame = clip.get_frame(1.0)  # 1 second frame
            temp_file = NamedTemporaryFile(delete=True, suffix='.jpg')
            from PIL import Image
            image = Image.fromarray(frame)
            image.save(temp_file, 'JPEG')
            self.thumbnail.save(os.path.basename(self.video_file.name) + '.jpg', File(temp_file))
            clip.close()
        except Exception as e:
            print(f"Thumbnail generation failed: {e}")
