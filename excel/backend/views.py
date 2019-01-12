from django.shortcuts import render
from io import BytesIO

import os

from urllib.parse import quote, unquote

import xlwt
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
from django.db import connections

from backend.models import Emp

from backend.models import Dept

PAGE_SIZE = 10

def agent_bar_data(request):
    names, totals = [], []
    # 可以通过django封装的connection和connections来获取数据库连接
    # 然后通过创建游标对象来发出原生SQL实现CRUD操作(性能更好)
    with connections['default'].cursor() as cursor:
        cursor.execute('select name, total from (select agentid, count(agentid) as total from tb_agent_estate group by agentid) t1 inner join tb_agent t2 on t1.agentid=t2.agentid')

        for row in cursor.fetchall():
            names.append(row[0])
            totals.append(row[1])
    # 将数据定制成JSON格式传递给浏览器
    # 如果data参数不是字典而是列表,还要加上safe=False参数
    # 如果字典或列中有自定义对象,那么还需要通过encoder参数指定自定义对象
    return JsonResponse({'names': names, 'totals':totals})


def home(request):
    return render(request, 'index.html')


def download(request):
    path = os.path.dirname(__file__)
    # with open(f'{path}/resources/Git手册.pdf', 'rb') as f:
    #     data = f.read()
    # 如果要动态生成PDF报表可以使用ReportLab三方库
    f = open(f'{path}/resources/Git手册.pdf', 'rb')
    f_iter = iter(lambda:f.read(4096), b'')
    resp = StreamingHttpResponse(f_iter, content_type='application/pdf')
    # 文件名包含中文,将其转换为百分号字符
    filename = quote('Git手册.pdf')
    # inline - 内联打开 / attachment - 附件下载
    resp['content-disposition'] = f'attachment; filename="{filename}"'
    return resp


def get_style(name, *, color=0, bold=False, italic=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.colour_index = color
    font.bold = bold
    font.italic = italic
    style.font = font
    return style

def export_emp_excel(request, page):
    # 创建excel工作簿
    workbook = xlwt.Workbook()
    # 向工作簿添加工作表
    sheet = workbook.add_sheet('员工信息')
    # 设置表头
    titles = ['编号', '姓名', '职位', '主管', '工资', '部门']
    for col, title in enumerate(titles):
        sheet.write(0, col, title, get_style(' ', color=2, bold=True))
    props = ('no', 'name', 'job', 'mgr', 'sal', 'dept')
    start = (page - 1) * PAGE_SIZE
    end = page * PAGE_SIZE
    # only(列),只查询几列而不是所有列
    # 在查询一个对象时,还要查询它的关联对象,
    # 必须对SQL语句进行优化,否则会引发1+N查询
    # 程序性能下降明显,数据库压力大
    # 如果有多对一关联,需要用连接查询加载关联对象,用select_related()来加载
    # 如果有多对多关联,需要用连接查询加载关联对象,用prefetch_related()来加载
    emps = Emp.objects.all().only(*props).select_related('dept').select_related('mgr').order_by('-sal')[start:end]
    # 通过数据库获得员工数据填写excel表格
    for row, emp in enumerate(emps):
        for col, prop in enumerate(props):
            val = getattr(emp, prop, '')
            if isinstance(val, (Dept, Emp)):
                val = val.name
            sheet.write(row+1, col, val)
    # 提取excel表格的数据 可写字节串
    buffer = BytesIO()
    workbook.save(buffer)
    # 生成响应对象传输数据给浏览器
    resp = HttpResponse(buffer.getvalue(), content_type='application/msexcel')
    filename = quote('员工信息表.xls')
    resp['content-disposition'] = f'attachment; filename="{filename}"'
    return resp





