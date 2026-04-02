from django.contrib import admin
from .models import * 
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Information", {
        'fields' : ('bio','avatar','phone_no','dob','role')
    }),
)
    
admin.site.register(User,CustomUserAdmin)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title','teacher','price','total_duration')
    search_fields = ('title',)
    ordering = ('teacher',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('course','order')
    list_filter = ("course",)
    ordering = ("course", "order",)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('students','course','date_entrolled')
    search_fields = ('students',)
    ordering = ('course',)

@admin.register(Category)
class Categoryadmin(admin.ModelAdmin):
    list_display = ('name','slug')
    search_fields = ('name',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student','transaction_id','course','status')
    search_fields = ('course','student')
    ordering = ('course',)

@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('students','lesson','get_course','is_completed')
    list_filter = ('is_completed','lesson__course')
    search_fields = ('student__username','lesson_notes')

    def get_course(Self,obj):
        return obj.lesson.course
    get_course.short_description = 'Course'

admin.site.register(Coupon)
