# -*- coding: utf-8 -*-
'''
按照SGS报告格式生成环境数据报告
'''
from datetime import datetime

# @Time : 2022/12/1 15:48
# @Author : LINYANZHEN
# @File : write_report.py
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Table, TableStyle
import os

PAGE_HEIGHT = A4[1]
PAGE_WIDTH = A4[0]
constan = "constan"
pdfmetrics.registerFont(TTFont(constan, "font/constan.ttf"))


def draw_page_background(c: Canvas, current_page: int, total_page: int):
    '''
    画每一页的背景，包括左上角的icon、标题、左上角页码、最底下的页脚（机构信息、报告日期等）

    :param c:
    :return:
    '''

    c.saveState()
    # 绘制左上角icon
    c.drawImage("picture/icon.png", 10, PAGE_HEIGHT - 100)
    # 绘制居中标题文本
    c.setFillColor(colors.orange)
    c.setFont(constan, 20)
    c.drawCentredString(300, PAGE_HEIGHT - 100, "Environment Report")
    # 写页面信息
    c.setFillColor(colors.black)
    c.setFont(constan, 12)
    c.drawString(500, PAGE_HEIGHT - 120, "Page {} of {}".format(current_page, total_page))
    c.setStrokeColor(colors.dimgrey)
    # 绘制线条
    c.line(30, PAGE_HEIGHT - 790, 570, PAGE_HEIGHT - 790)
    # 绘制页脚文字
    c.setFont(constan, 12)
    c.setFillColor(colors.black)
    date = datetime.today().date()
    c.drawString(30, PAGE_HEIGHT - 810, "Report Date: {}".format(date))
    c.restoreState()


def draw_first_page(c: Canvas):
    '''
    画第一页 封面内容，包含标题、客户资料表格、评论内容栏、签名栏

    :param c:
    :return:
    '''
    draw_page_background(c, 1, 2)
    c.setFillColor(colors.black)
    c.setFont(constan, 15)
    c.drawString(70, PAGE_HEIGHT - 180, "CLIENT DETAILS              LABORATORY DETAILS")
    # 画客户资料表格
    data = [
        ["Contact: ", "EDMUND LEI", "Manager", "SGS HONG KONG LIMITED"],
        ["Client: ", "", "Laboratory: ", ""],
        ["Address: ", "", "Address: ", ""],
        ["Telephone: ", "", "Telephone: ", ""],
        ["Facsimile: ", "", "Facsimile: ", ""],
        ["Email: ", "", "Email: ", ""],
        ["Order Number: ", "", "Report Number: ", ""],
        ["Samples: ", "", "SGS Reference: ", ""],
        ["Project: ", "", "Date Reported: ", datetime.today().date()],
    ]
    table = Table(data, style={
        ("Font", (0, 0), (-1, -1), constan, 12),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.gray),
        ("TEXTCOLOR", (2, 0), (2, -1), colors.gray),
        ("TEXTCOLOR", (1, 0), (1, -1), colors.black),
        ("TEXTCOLOR", (3, 0), (3, -1), colors.black),
        ('ALIGN', (1, 0), (1, -1), 'LEFT')
    })
    table.wrapOn(c, 0, 0)
    table.drawOn(c, 50, PAGE_HEIGHT - 350)
    # 写评论
    c.setFillColor(colors.black)
    c.setFont(constan, 15)
    c.drawString(70, PAGE_HEIGHT - 400, "COMMENTS")
    # 签名栏
    c.setFillColor(colors.black)
    c.setFont(constan, 15)
    c.drawString(70, PAGE_HEIGHT - 600, "SIGNATORIES")
    c.showPage()


def draw_second_page(c: Canvas):
    draw_page_background(c, 2, 2)


# 创建文档
# doc = SimpleDocTemplate("report/test.pdf")
# Story = [Spacer(1, 2 * inch)]
# # 保存文档
# doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
save_pdf = "report/test.pdf"
if os.path.exists(save_pdf):
    os.remove(save_pdf)
c = Canvas(save_pdf)
c.setPageSize(A4)
draw_first_page(c)
draw_second_page(c)
c.save()
