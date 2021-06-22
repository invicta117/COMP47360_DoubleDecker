'''
This model is for Mysql. We then create the dao level to map the field
'''
from sqlalchemy import Column, Integer, String, DATETIME, DATE, TIME
from sqlalchemy.ext.declarative import declarative_base

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

Base_Leave = declarative_base()

class RT_LeaveTimes(Base_Leave):
    __tablename__ = 'RT_Trips'
    tripId = Column('tripId', Integer, primary_key=True)
    dataSource = Column('dataSource', String(100))
    dayOfService = Column('dayOfService', DATE)
    progrNumber = Column('progrNumber', Integer)
    stopId = Column('stopId', Integer)
    plannedTime_Arr = Column('plannedTime_Arr', TIME)
    plannedTime_Dep = Column('plannedTime_Dep', TIME)
    actualTime_arr = Column('actualTime_arr', TIME)
    actualTime_Dep = Column('actualTime_Dep', TIME)
    vehicleId = Column('vehicleId', Integer)
    passengers = Column('passengers', Integer)
    passengersIn = Column('passengersIn', Integer)
    passengersOut = Column('passengersOut', Integer)
    distance = Column('distance', Integer)
    suppressed = Column('suppressed', String(100))
    justificationId = Column('justificationId', Integer)
    lastUpdate = Column('lastUpdate', DATETIME)
    note = Column('note', String(50))