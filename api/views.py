from django.shortcuts import render, HttpResponse, redirect
from api import models
# Create your views here.


def index(request):

    # 业务逻辑

    # 返回请求

    # return HttpResponse('index')
    return render(request, 'index.html')  # 返回html页面


def login(request):

    if request.method == 'POST':
        # 处理post请求
        # 获取到用户提交的用户名和密码
        user = request.POST.get('user')
        password = request.POST.get('password')
        # 进行校验
        if models.User.objects.filter(username=user, password=password):
            # 校验成功，告知登陆成功
            return redirect('/index/')
            # 使用重定向返回,使用render返回地址不会改变
            # return render(request, 'login2.html')
    return render(request, 'login.html')


def department_list(request):
    # 返回所有院系的信息
    # 获取所有的院系
    all_department = models.Department.objects.all().order_by('dept_id')  # 对象列表

    # 返回页面
    return render(request, 'department_list.html', {'all_department': all_department})


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


def department_del(request):

    del_id = request.GET.get('dept_id')
    models.Department.objects.filter(pk=del_id).delete()  # 使用filter代替get避免不存在时报错
    return redirect('/department_list/')


def department_edit(request):
    pk = request.GET.get('dept_id')
    dept_obj = models.Department.objects.get(pk=pk)
    if request.method == 'GET':
        return render(request, 'department_edit.html', {'dept_boj':dept_obj})
    else:
        dept_obj.dept_id = request.POST.get('dept_id')
        dept_obj.dept_name = request.POST.get('dept_name')
        dept_obj.address = request.POST.get('dept_address')
        dept_obj.save()
        return redirect('/department_list/')
