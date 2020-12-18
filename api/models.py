from django.db import models
from django.utils import timezone
# Create your models here.


class User(models.Model):

    username = models.CharField(max_length=32)  # varchar(32)
    password = models.CharField(max_length=32)  # varchar(32)

    def __str__(self):
        return self.username

    class Meta:  # admin 中配置
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class Department(models.Model):

    dept_id = models.AutoField(primary_key=True)
    dept_name = models.CharField(max_length=32)
    address = models.CharField(max_length=32)

    def __str__(self):
        return self.dept_name

    class Meta:  # admin 中配置
        verbose_name = '院系'
        verbose_name_plural = verbose_name


class Student(models.Model):

    student_id = models.IntegerField(primary_key=True)
    student_name = models.CharField(max_length=32)
    student_age = models.IntegerField(null=True, blank=True)
    student_sex = models.CharField(max_length=10)
    person_id = models.CharField(max_length=32)
    phone_number = models.CharField(max_length=32)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)  # 级联删除

    def __str__(self):
        return self.student_name

    class Meta:  # admin 中配置
        verbose_name = '学生'
        verbose_name_plural = verbose_name


class Teacher(models.Model):

    teacher_id = models.IntegerField(primary_key=True)
    teacher_name = models.CharField(max_length=32)
    teacher_age = models.IntegerField(null=True, blank=True)
    teacher_sex = models.CharField(max_length=10)
    person_id = models.CharField(max_length=32)
    phone_number = models.CharField(max_length=32)
    salary = models.IntegerField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)  # 级联删除

    def __str__(self):
        return self.teacher_name

    class Meta:  # admin 中配置
        verbose_name = '教师'
        verbose_name_plural = verbose_name


class Course(models.Model):

    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=32)
    course_credit = models.IntegerField(null=True, blank=True)
    course_place = models.CharField(max_length=32)
    course_time = models.CharField(max_length=32)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)  # 级联删除
    department = models.ForeignKey(Department, on_delete=models.CASCADE)  # 级联删除

    def __str__(self):
        return self.course_name

    class Meta:  # admin 中配置
        verbose_name = '课程'
        verbose_name_plural = verbose_name


class Award(models.Model):

    award_id = models.AutoField(primary_key=True)
    award_type = models.CharField(max_length=10)
    award_reason = models.CharField(max_length=100)
    award_time = models.DateTimeField(default=timezone.now)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.award_type

    class Meta:  # admin 中配置
        verbose_name = '奖惩'
        verbose_name_plural = verbose_name


class student_course(models.Model):

    student_course_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    retake = models.IntegerField(default=0)
    score = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.student_course_id)

    class Meta:  # admin 中配置
        verbose_name = '选课'
        verbose_name_plural = verbose_name