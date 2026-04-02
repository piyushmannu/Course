from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractUser
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction


# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = (
        ('student','Student'),
        ('teacher',"Teacher")
    )
    role = models.CharField(max_length=10,choices=ROLE_CHOICES)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/',null = True, blank = True)
    phone_no = models.CharField(max_length=15,blank = True)
    dob = models.DateField(null=True,blank= True)
    is_verified = models.BooleanField(default=False)

    def is_student(self):
        return self.role == 'student'
    
    def is_teacher(self):
        return self.role == 'teacher'
    
class Category(models.Model):
    name =models.CharField(max_length=50,unique=True)
    slug = models.SlugField(max_length=50,unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey("self",on_delete = models.CASCADE,null=True,blank=True,related_name="subcategories")
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='categories')
    created_at = models.DateField(auto_now_add = True)

    class Meta : 
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Course(models.Model):
    id = models.SlugField(primary_key=True)
    category = models.ManyToManyField(Category,related_name='courses')
    title = models.CharField(max_length=50)
    thumbnail = models.ImageField(upload_to='thumbnails/%Y/%m/',blank=True,null=True)
    price = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)

    @property
    def total_duration(self):
        total_minutes = sum(lesson.duration for lesson in self.lessons.all())

        #calcualte hour and minutes
        hour = total_minutes // 60
        minutes = total_minutes % 60

        #returning a value
        if hour > 0:
            return f"{hour}h {minutes}m"
        return f"{minutes}m" 

    teacher = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='course')
    
    def __str__(self):
        return self.title
    
class Lesson(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='lessons')
    video = models.FileField(upload_to='lessons/%Y/%m/',blank=True,null=True)
    notes = models.TextField(max_length=50)
    order = models.PositiveBigIntegerField()
    duration = models.IntegerField()
    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.order}"
    
class LessonProgress(models.Model):
    students = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE,related_name='progress')
    is_completed = models.BooleanField(default=False)
    completed_at=models.DateTimeField(null=True,blank=True)

    class Meta:
        #a student should only have one progress per lesson
        unique_together = ('students','lesson')

    def mark_as_complete(self):
        self.is_completed = True
        self.completed_at = timezone.now()
        self.save()

    def __str__(self):
        status = 'Done' if self.is_completed else "In Progress"
        return f"{self.students.username} - {self.lesson.order} ({status})"    
    
class Enrollment(models.Model):
    students = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    date_entrolled = models.DateTimeField(auto_now_add=True)

    class Meta :
        unique_together = ('students','course')

class Coupon(models.Model):
    code = models.CharField(max_length=20,unique=True)
    discount_percent = models.IntegerField()
    valid_from = models.DateField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)

class Payment(models.Model):
    STATUS_CHOICES = (
        ('pending','Pending'),
        ('completed','Completed'),
        ('failed','Failed'),
    )

    #Generate a unique transaction ID for each attempt
    transaction_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True,db_index=True)
    student = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price at time of purchase")  
    coupon = models.ForeignKey(Coupon,on_delete=models.SET_NULL,null=True,blank=True)  
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # If this is a new payment, grab the price from the course automatically
        if not self.amount_paid:
            self.amount_paid = self.course.price
        super().save(*args, **kwargs)

    @transaction.atomic
    def process_payment(student,course):
        payment = Payment.objects.create(
            student = student, course = course, amount_paid = course.price, status = "completed")

    def __str__(self):
        return f"{self.student.username} - {self.course.title} ({self.status})"
    
# --- The Magic Logic (Signals) ---
@receiver(post_save, sender=Payment)
def create_enrollment_on_payment(sender,instance,created,**kwargs):
    """
    When a payment is updated to 'completed', automatically create an enrollment
    """
    if instance.status == 'completed':
        # FETCHING THE PRICE:
        # Access the related course, then its price field
        actual_course_price = instance.course.price

        print(f"User paid {actual_course_price} for {instance.course.title}")
        # get_or_create prevents duplicate enrollments if the admin saves twice
        Enrollment.objects.get_or_create(
            students=instance.student,
            course=instance.course
        )

class review(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student','course')

