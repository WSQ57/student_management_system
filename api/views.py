from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
import csv
import codecs
import json
import xlwt
from api import models


# Create your views here.


def index(request):
    # 业务逻辑

    # 返回请求

    # return HttpResponse('index')
    return render(request, 'index.html')  # 返回html页面


def user_login(request):
    if request.method == 'POST':
        response_json_data = {}
        data = json.loads(request.body)
        username = data["username"]
        password = data["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response_json_data["code"] = 200
            response_json_data["msg"] = "登入成功"
            if models.Student.objects.filter(pk=username):
                response_json_data['type'] = "student"
            else:
                response_json_data['type'] = "teacher"
            return JsonResponse(response_json_data)
        else:
            print(username)
            response_json_data["code"] = 404
            response_json_data["msg"] = "用户不存在"
            return JsonResponse(response_json_data)
            # return render(request, 'login2.html', {'error': '账号或密码错误'})

    # if request.method == 'POST':
    #     # 处理post请求
    #     # 获取到用户提交的用户名和密码
    #     user_name = request.POST.get('user')
    #     password = request.POST.get('password')
    #     user=authenticate(request,username = user_name,password = password)
    #     if user is not None:
    #         login(request,user)
    #         # logout(request)
    #         return redirect('/student_elective/')
    #     else:
    #         return render(request, 'login.html',{'error': '账号或密码错误'})

    return render(request, 'login2.html')


def user_logout(request):
    logout(request)
    return redirect('/login/')


@login_required(login_url='/login/')
def department_list(request):
    # 返回所有院系的信息
    # 获取所有的院系
    all_department = models.Department.objects.all().order_by('dept_id')  # 对象列表

    # 返回页面
    return render(request, 'department_list.html', {'all_department': all_department})


@login_required(login_url='/login/')
def department_add(request):
    if request.method == 'POST':
        dept_id = request.POST.get('dept_id')
        dept_name = request.POST.get('dept_name')
        dept_address = request.POST.get('dept_address')
        if not dept_id or not dept_name or not dept_address:
            return render(request, 'department_add.html', {'error': '输入数据不能为空'})

        if models.Department.objects.filter(dept_id=dept_id):
            return render(request, 'department_add.html', {'error1': '院系id已存在'})

        if models.Department.objects.filter(dept_name=dept_name):
            return render(request, 'department_add.html', {'error2': '院系名称已存在'})

        models.Department.objects.create(dept_name=dept_name, dept_id=dept_id, address=dept_address)
        return redirect('/department_list/')

    return render(request, 'department_add.html')


@login_required(login_url='/login/')
def department_del(request):
    del_id = request.GET.get('dept_id')
    models.Department.objects.filter(pk=del_id).delete()  # 使用filter代替get避免不存在时报错
    return redirect('/department_list/')


@login_required(login_url='/login/')
def department_edit(request):
    pk = request.GET.get('dept_id')
    dept_obj = models.Department.objects.get(pk=pk)
    if request.method == 'GET':
        return render(request, 'department_edit.html', {'dept_boj': dept_obj})
    else:
        dept_obj.dept_id = request.POST.get('dept_id')
        dept_obj.dept_name = request.POST.get('dept_name')
        dept_obj.address = request.POST.get('dept_address')
        dept_obj.save()
        return redirect('/department_list/')


@login_required(login_url='/login/')
def course_list(request):
    all_course = models.Course.objects.all()
    return render(request, 'course_list.html', {'all_course': all_course})


@login_required(login_url='/login/')
def course_add(request):
    if request.method == 'POST':
        c_id = request.POST.get('c_id')
        c_name = request.POST.get('c_name')
        c_credit = request.POST.get('c_credit')
        c_address = request.POST.get('c_address')
        c_time = request.POST.get('c_time')
        teacher = request.POST.get('teacher')
        department = request.POST.get('department')
        models.Course.objects.create(course_id=c_id, course_name=c_name, course_credit=c_credit,
                                     course_place=c_address, course_time=c_time, teacher_id=teacher,
                                     department_id=department)
        return redirect('/course_list/')

    all_teacher = models.Teacher.objects.all()
    all_department = models.Department.objects.all()
    return render(request, 'course_add.html', {'all_teacher': all_teacher, 'all_department': all_department})


@login_required(login_url='/login/')
def course_del(request):
    del_id = request.GET.get('course_id')
    self_id = request.user.username
    a = models.student_course.objects.get(course_id=del_id, student_id=self_id)
    if a.retake == 1:
        a.update(retake=0)
    else:
        models.student_course.objects.filter(course_id=del_id, student_id=self_id).delete()

    return render(request, 'self_course.html', {'error': '退课成功'})


@login_required(login_url='/login/')
def student_elective(request):
    c_id = request.POST.get('c_id')
    if request.method == 'POST' and c_id != "":
        all_course = models.Course.objects.filter(pk=c_id)
    else :
        all_course = models.Course.objects.all()
    paginator = Paginator(all_course, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'student_elective.html', {'page_obj': page_obj})

    # return render(request, 'student_elective.html', {'all_course': all_course})


@login_required(login_url='/login/')
def elect_course(request):
    s_id = request.user.username
    c_id = request.GET.get('course_id')
    if models.student_course.objects.filter(course_id=c_id, student_id=s_id):
        return render(request, 'student_elective.html', {'error': '该门课已选过'})
    t_id = models.Course.objects.get(pk=c_id).teacher_id
    models.student_course.objects.create(student_id=s_id, course_id=c_id, teacher_id=t_id)
    return render(request, 'student_elective.html', {'error': '选课成功'})


@login_required(login_url='/login/')
def self_course(request):

    s_id = request.user.username
    c_id = request.POST.get('c_id')
    if request.method == 'POST' and c_id != "":
        all_elective = models.student_course.objects.filter(course_id=c_id,student_id=s_id)
    else: all_elective = models.student_course.objects.filter(student_id=s_id)

    return render(request, 'self_course.html', {'all_elective': all_elective})


@login_required(login_url='/login/')
def self_information(request):
    s_id = request.user.username
    information = models.Student.objects.get(pk=s_id)
    return render(request, 'self_information.html', {'information': information})


@login_required(login_url='/login/')
def history_course(request):
    s_id = request.user.username
    c_id = request.POST.get('c_id')
    if request.method == 'POST' and c_id != "":
        all_elective = models.student_course.objects.filter(course_id=c_id,student_id=s_id)
    else:
        all_elective = models.student_course.objects.filter(student_id=s_id)

    return render(request, 'history_course.html', {'all_elective': all_elective})


@login_required(login_url='/login/')
def export_users_csv(request):
    s_id = request.user.username
    response = HttpResponse(content_type='text/csv')
    response.write(codecs.BOM_UTF8)
    response['Content-Disposition'] = 'attachment; filename="course.csv"'
    writer = csv.writer(response)
    writer.writerow(['course_id', 'course_name', 'course_credit', 'teacher_name', 'course_grade'])
    courses = models.student_course.objects.filter(~Q(score=None), student_id=s_id).values_list('course_id',
                                                                                                'course__course_name',
                                                                                                'course__course_credit',
                                                                                                'course__teacher__teacher_name',
                                                                                                'score')
    for course in courses:
        writer.writerow(course)
    return response


@login_required(login_url='/login/')
def export_users_xls(request):
    s_id = request.user.username
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="courses.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('courses')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['course_id', 'course_name', 'course_credit', 'teacher_name', 'course_grade']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    courses = models.student_course.objects.filter(~Q(score=None), student_id=s_id).values_list('course_id',
                                                                                                'course__course_name',
                                                                                                'course__course_credit',
                                                                                                'course__teacher__teacher_name',
                                                                                                'score')
    for course in courses:
        row_num += 1
        for col_num in range(len(course)):
            ws.write(row_num, col_num, course[col_num], font_style)
    wb.save(response)
    return response


@login_required(login_url='/login/')
def teacher_management(request):
    t_id = request.user.username
    s_id = request.POST.get('s_id')
    if request.method == 'POST' and s_id != "":
        courses = models.student_course.objects.filter(student_id=s_id,teacher_id=t_id)
    else:
        courses = models.student_course.objects.filter(teacher_id=t_id).order_by('course_id')
    paginator = Paginator(courses, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'teacher_management.html', {'page_obj': page_obj})


@login_required(login_url='/login/')
def score_edit(request):
    pk = request.GET.get('sc_id')
    sc_obj = models.student_course.objects.filter(pk=pk)
    if request.method == 'GET':
        return render(request, 'course_edit.html')
    else:
        for i in sc_obj:
            if i.retake == 1 and int(request.POST.get('score')) < i.score:
                return render(request, 'course_edit.html', {'error': '重修成绩不应比原来低'})

        sc_obj.update(score=request.POST.get('score'))
        sc_obj.update(retake=0)
        return redirect('/teacher_management/')


@login_required(login_url='/login/')
def teacher_course(request):
    t_id = request.user.username
    c_id = request.POST.get('c_id')
    if request.method == 'POST' and c_id != "":
        all_courses = models.Course.objects.filter(course_id=c_id, teacher_id=t_id)
    else: all_courses = models.Course.objects.filter(teacher_id=t_id)
    return render(request, 'teacher_course.html', {'all_courses': all_courses})


@login_required(login_url='/login/')
def teacher_information(request):
    t_id = request.user.username
    information = models.Teacher.objects.get(pk=t_id)
    return render(request, 'teacher_information.html', {'information': information})


@login_required(login_url='/login/')
def my_students(request):
    t_id = request.user.username
    s_id = request.POST.get('s_id')
    if request.method == 'POST' and s_id != "":
        sc = models.student_course.objects.filter(student_id=s_id,teacher_id=t_id)
    else: sc = models.student_course.objects.filter(teacher_id=t_id).order_by('course__course_name')
    return render(request, 'my_students.html', {'sc': sc})


@login_required(login_url='/login/')
def export_students_csv(request):
    t_id = request.user.username
    response = HttpResponse(content_type='text/csv')
    response.write(codecs.BOM_UTF8)
    response['Content-Disposition'] = 'attachment; filename="students.csv"'
    writer = csv.writer(response)
    writer.writerow(['course_id', 'course_name', 'student_id', 'student_name', 'retake'])
    students = models.student_course.objects.filter(teacher_id=t_id).values_list('course_id',
                                                                                'course__course_name',
                                                                                'student_id',
                                                                                'student__student_name',
                                                                                'retake')
    for student in students:
        writer.writerow(student)
    return response


@login_required(login_url='/login/')
def export_students_xls(request):
    t_id = request.user.username
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="students.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('students')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['course_id', 'course_name', 'student_id', 'student_name', 'retake']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    students = models.student_course.objects.filter(teacher_id=t_id).values_list('course_id',
                                                                                'course__course_name',
                                                                                'student_id',
                                                                                'student__student_name',
                                                                                'retake')
    for student in students:
        row_num += 1
        for col_num in range(len(student)):
            ws.write(row_num, col_num, student[col_num], font_style)
    wb.save(response)
    return response



@login_required(login_url='/login/')
def retake_course(request):
    s_id = request.user.username
    c_id = request.GET.get('course_id')
    t_id = models.Course.objects.get(pk=c_id).teacher_id
    models.student_course.objects.update(retake=1)
    return render(request, 'history_course.html', {'error': '重修选课成功'})