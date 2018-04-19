#-*- coding:utf-8 -*-
from sqlalchemy import create_engine
import tushare as ts
import Log
import os

sql_str='mysql://root:sys@localhost/gp?charset=utf8'

# 行业分类
def exportIndustry(fromDate, toDate, code):
    df = ts.get_industry_classified()
    engine = create_engine(sql_str)
    # 存入数据库
    df.to_sql('industry_classified', engine, if_exists='append')
    Log.logger.info("industry_classified数据导入完成。")
    return True

# 概念分类
def exportConcept_classified(fromDate, toDate, code):
    df = ts.get_concept_classified()
    engine = create_engine(sql_str)
    # 存入数据库
    df.to_sql('concept_classified', engine, if_exists='append')
    Log.logger.info("concept_classified数据导入完成。")
    return True

# 风险警示板分类(垃圾股票)
def exportSt_classified(fromDate, toDate, code):
    df = ts.get_st_classified()
    engine = create_engine(sql_str)
    # 存入数据库
    df.to_sql('st_classified', engine, if_exists='append')
    Log.logger.info("st_classified数据导入完成。")
    return True

# 大单交易数据
def exportDadan(fromDate, toDate, code):
    df = ts.get_sina_dd(code, toDate)
    engine = create_engine(sql_str)
    table_name = "dadan_" + code + "_" + toDate.replace("-", "", 3)
    # 存入数据库
    df.to_sql('dadan', engine, if_exists='append')
    Log.logger.info("dadan数据导入完成。")
    return True

# 历史分笔
def exportTick_data(fromDate, toDate, code):
    df = ts.get_tick_data()
    engine = create_engine(sql_str)
    # 存入数据库
    df.to_sql('tick_data', engine, if_exists='append')
    Log.logger.info("tick_data数据导入完成。")
    return True

# 实时分笔
def exportRealtime_quotes(fromDate, toDate, code):
    df = ts.get_realtime_quotes(code)
    engine = create_engine(sql_str)
    # 存入数据库
    df.to_sql('realtime_quotes', engine, if_exists='append')
    Log.logger.info("realtime_quotes数据导入完成。")
    return True

# 实时行情
def exportToday_all(fromDate, toDate, code):
    df = ts.get_today_all()
    engine = create_engine(sql_str)
    # 存入数据库
    df.to_sql('today_all', engine, if_exists='append')
    Log.logger.info("today_all数据导入完成。")
    return True

# 历史行情
def export_hist_data(fromDate, toDate, code):
    df = ts.get_hist_data(code,ktype='M')
    engine = create_engine(sql_str)
    tableName = "hist_data_" + code
    # 存入数据库
    df.to_sql(tableName, engine, if_exists='append')
    Log.logger.info("hist_data数据导入完成。")
    return True


