from django.contrib import admin
from api import models
# Register your models here.

# Register your models here.


class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_name','student_id','person_id']


class TeacherAdmin(admin.ModelAdmin):
    list_display = ['teacher_name','teacher_id','person_id']


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['dept_id','dept_name','address']


class AwardAdmin(admin.ModelAdmin):
    list_display = ['award_id','award_type','award_reason', 'award_time','student']


class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_id','course_name','course_credit','course_place','course_time','teacher','department']


class SCAdmin(admin.ModelAdmin):
    list_display = ['student_course_id','student','course','teacher','retake','score']


admin.site.register(models.Student,StudentAdmin)
admin.site.register(models.Teacher,TeacherAdmin)
admin.site.register(models.Department,DepartmentAdmin)
admin.site.register(models.Award,AwardAdmin)
admin.site.register(models.Course,CourseAdmin)
admin.site.register(models.student_course,SCAdmin)
