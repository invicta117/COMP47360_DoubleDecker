from sqlalchemy import Column, Integer, String, DATETIME, DATE, TIME
from sqlalchemy.ext.declarative import declarative_base

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

Rt_Trip = declarative_base()

'''
use the Mysql to create the model
'''
class RT_Trips(Rt_Trip):
    __tablename__ = 'RT_Trips'
    tripId = Column('tripId', Integer, primary_key=True)
    dataSource = Column('dataSource', String(100))
    dayOfService = Column('dayOfService', DATE)
    lineId = Column('lineId', String(50))
    routeId = Column('routeId', String(50))
    direction = Column('direction', String(40))
    plannedTime_Arr = Column('plannedTime_Arr', TIME)
    plannedTime_Dep = Column('plannedTime_Dep', TIME)
    actualTime_arr = Column('actualTime_arr', TIME)
    actualTime_Dep = Column('actualTime_Dep', TIME)
    basin = Column('basin', String(100))
    tenderLot = Column('tenderLot', String(80))
    suppressed = Column('suppressed', String(100))
    justificationId = Column('justificationId', Integer)
    lastUpdate = Column('lastUpdate', DATE)
    note = Column('note', String(50))
