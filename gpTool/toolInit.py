#-*- coding:utf-8 -*-

from PyQt5.QtCore import QDate
from sqlalchemy import create_engine
import tushare as ts

import sys
import os,os.path
import Log
import crawWeb

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5 import QtPrintSupport, QtWidgets
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox

#
# def zuixiaoerchen(arrayY, picTitle):
#     print(f"arrayY: {arrayY}")
#     print(f"picTitle: {picTitle}")
#
#     if len(arrayY) == 0:
#         return [0, 0, 0]
#
#     # 取得最大销量，作为纵坐标的峰值标准
#     maxValue = max(arrayY)
#
#     # 设置横坐标和纵坐标的值
#     # def arange(start=None, stop=None, step=None, dtype=None)
#     x = numpy.arange(1, len(arrayY) + 1, 1)
#
#     # def array(p_object, dtype=None, copy=True, order='K', subok=False, ndmin=0)
#     y = numpy.array(arrayY)
#
#     # 第1個拟合，设置自由度為1 : (y = ax + b)
#     z = numpy.polyfit(x, y, 1)
#     # z: [  0.46428571  13.35238095]
#     print(f"z: {z}")
#
#     # 生成的多項式對象(y = ax + b)
#     p = numpy.poly1d(z)
#     # p: -0.1448x + 13.23
#     print(f"p: {p}")
#
#     if z[0] > 0:
#
#         # 绘制原曲线及 拟合后的曲线
#
#         # 原曲线 , 设置颜色(蓝色)和标签
#         pylab.plot(x, y, 'b^-', label='original sales growth')
#
#         # 自由度为1的趋势曲线, 设置颜色(蓝色)和标签
#         pylab.plot(x, p(x), 'gv--', label=f'y = {z[0]}x + {z[1]}')
#
#         # 设置图表的title
#         pylab.title(f"picTitle: {picTitle}")
#
#         # 设置横坐标，纵坐标的范围 [xmin=0, xmax=16, ymin=0, ymax=30]
#         pylab.axis([0, len(arrayY) + 1, 0, maxValue + 1])
#         pylab.legend()
#
#         # 保存成图片，需要提前创建文件夹 Growth，程序不会自动创建
#         pylab.savefig(f"Growth/{picTitle}.png", dpi=96)
#
#         # 清除图表设置，以防止曲线多次累计
#         # 如果不清除，那么在这个程序运行起见，多次调用这个函数时，会不断将之前的曲线累计到新图片中
#         pylab.clf()
#
#     return [z[0], z[1], maxValue]


# 用最小二乘法，生成销量趋势
# sales = [10, 15, 8, 20, 16, 19, 11, 30, 21, 15, 19, 17, 16, 22, 17]
# a, b, maxSale = zuixiaoerchen(sales, "sales Growth")
# growth = a
# maxSale = maxSale


class Tool(QtWidgets.QWidget):
    def __init__(self):
        super(Tool, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(150, 150, 800, 450)
        self.setWindowTitle('gp tool')

        self.label = QtWidgets.QLabel("日期(From-To):", self)
        self.label.setGeometry(QtCore.QRect(50, 100, 100, 30))

        # combo.activated.connect(self.onActivated)
        self.textEditF = QtWidgets.QDateEdit(self)
        self.textEditF.setGeometry(QtCore.QRect(150, 100, 100, 30))
        self.textEditF.setDisplayFormat("yyyy-MM-dd")
        self.textEditF.setObjectName("fromEdit")
        self.textEditF.setDate(QDate.currentDate())

        # combo.activated.connect(self.onActivated)
        self.label2 = QtWidgets.QLabel("--", self)
        self.label2.setGeometry(QtCore.QRect(260, 100, 20, 30))

        # combo.activated.connect
        self.textEditT = QtWidgets.QDateEdit(self)
        self.textEditT.setDisplayFormat("yyyy-MM-dd")
        self.textEditT.setGeometry(QtCore.QRect(290, 100, 100, 30))
        self.textEditT.setObjectName("toEdit")
        self.textEditT.setDate(QDate.currentDate())

        # combo.activated.connect(self.onActivated)
        self.label3 = QtWidgets.QLabel("code：", self)
        self.label3.setGeometry(QtCore.QRect(50, 140, 100, 30))

        self.textEditCode = QtWidgets.QTextEdit(self)
        self.textEditCode.setGeometry(QtCore.QRect(150, 140, 100, 30))
        self.textEditCode.setObjectName("textEdit")

        # combo.activated.connect(self.onActivated)
        self.label4 = QtWidgets.QLabel("表名：", self)
        self.label4.setGeometry(QtCore.QRect(260, 140, 50, 30))

        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.addItem("industry_classified")
        self.comboBox.addItem("concept_classified")
        self.comboBox.addItem("st_classified")
        self.comboBox.addItem("dadan")
        self.comboBox.addItem("tick_data")
        self.comboBox.addItem("realtime_quotes")
        self.comboBox.addItem("today_all")
        self.comboBox.addItem("hist_data")
        self.comboBox.setGeometry(QtCore.QRect(315, 140, 150, 30))

        encryptButton = QtWidgets.QPushButton(self)
        encryptButton.setText("导出")
        encryptButton.setGeometry(QtCore.QRect(120, 180, 60, 35))
        encryptButton.setObjectName("encryptButton")
        encryptButton.clicked.connect(self.exportEvent)

    # 不常用表导出
    def exportEvent(self, *args, **kwargs):
        kbn = self.comboBox.currentText()
        fromValue = self.textEditF.text()
        toValue = self.textEditT.text()
        gpValue = self.textEditCode.toPlainText()

        result = None
        # 行业分类
        try:
            if kbn == "industry_classified":
                result = crawWeb.exportIndustry(fromValue, toValue, gpValue)
            elif kbn == "concept_classified":
                #概念分类
                result = crawWeb.exportConcept_classified(fromValue, toValue, gpValue)
            elif kbn == "st_classified":
                #风险警示板分类(垃圾股票)
                result = crawWeb.exportSt_classified(fromValue, toValue, gpValue)
            elif kbn == "dadan":
                result = crawWeb.exportDadan(fromValue, toValue, gpValue)
            elif kbn == "tick_data":
                #历史分笔
                result = crawWeb.exportTick_data(fromValue, toValue, gpValue)
            elif kbn == "realtime_quotes":
                #实时分笔
                result = crawWeb.exportRealtime_quotes(fromValue, toValue, gpValue)
            elif kbn == "today_all":
                # 实时行情
                result = crawWeb.exportToday_all(fromValue, toValue, gpValue)
            elif kbn == "hist_data":
                # 历史行情
                result = crawWeb.export_hist_data(fromValue, toValue, gpValue)
            else:
                result = crawWeb.exportIndustry(fromValue, toValue, gpValue)
        except Exception as ex:
            Log.logger.error(ex.with_traceback())
            print(ex)

        result_reply = None
        if result:
            result_reply = QMessageBox.information(self, "结果", "导入成功。<br/>表名:" + kbn)
        else:
            result_reply = QMessageBox.information(self, "结果", "导入失败。", QMessageBox.Ok)

        if result_reply == QMessageBox.Ok:
            return


if __name__ == '__main__':

    try:
        app = QtWidgets.QApplication([])
        ex = Tool()
        ex.show()
        sys.exit(app.exec_())
    except QtWidgets.QErrorMessage as e:
        Log.logger.error(e.showMessage())
        print (e.showMessage())
    except Exception as ex:
        Log.logger.error(ex.showMessage())
        print (ex.showMessage())