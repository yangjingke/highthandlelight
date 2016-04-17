from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

CONN_STRING = 'mysql://gaogandeng:123456@223.3.41.132:3306/gaogandeng'
DEBUG = True

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer(), primary_key=True)
    user_name = Column(String(45))
    password = Column(String(45))
    authority = Column(Integer())
    phone = Column(String(45))
    address = Column(Text())

    controllogs = relationship("Controllog", backref=backref('user'))

    def __repr__(self):
        return "User(user_id='{self.user_id}', " \
                    "user_name='{self.user_name}', " \
                    "authority='{self.authority}')".format(self=self)


class Light(Base):
    __tablename__ = "lights"

    id = Column(Integer(), primary_key=True)
    device_id = Column(String(45))
    group_id = Column(String(45))
    in_group_id = Column(String(45))

    lightcontrollogs = relationship("Lightcontrollog", backref=backref('light', order_by=id))
    lightstatuslogs = relationship("Lightstatuslog", backref=backref('light', order_by=id))
    warninglogs = relationship("Warninglog", backref=backref('light', order_by=id))

    def __repr__(self):
        return "Light(id='{self.id}', " \
                     "device_id='{self.device_id}', " \
                     "group_id='{self.group_id}', " \
                     "in_group_id='{self.in_group_id}')".format(self=self)


class Controllog(Base):
    __tablename__ = "controllogs"

    id = Column(Integer(), primary_key=True)
    open_time = Column(DateTime())
    close_time = Column(DateTime())
    control_user_id = Column(Integer(), ForeignKey('users.user_id'))
    light_ids = Column(String(500))
    status = Column(Integer())
    cmd = Column(Integer())
    bright = Column(Integer())

    def __repr__(self):
        return "Controllog(id='{self.id}', " \
                          "open_time='{self.open_time}', " \
                          "close_time='{self.close_time}', " \
                          "control_user_id='{self.control_user_id}', " \
                          "light_ids='{self.light_ids}', " \
                          "status='{self.status}', " \
                          "cmd='{self.cmd}', " \
                          "bright='{self.bright}')".format(self=self)



class Lightcontrollog(Base):
    __tablename__ = "lightcontrollogs"

    id = Column(Integer(), primary_key=True)
    light_id = Column(Integer(), ForeignKey('lights.id'))
    cmd = Column(Integer())
    bright = Column(Integer())
    status = Column(Integer())
    cmd_time = Column(DateTime())

    def __repr__(self):
        return "Lightcontrollog(id='{self.id}')".format(self=self)
        

class Lightstatuslog(Base):
    __tablename__ = "lightstatuslogs"

    id = Column(Integer(), primary_key=True)
    light_id = Column(Integer(), ForeignKey('lights.id'))
    light_vol = Column(Float())
    light_cur = Column(Float())
    light_pow = Column(Float())
    light_bright = Column(Integer())
    envi_bright = Column(Integer())
    temperature = Column(Float())
    temperature1=Column(Float())
    temperature2=Column(Float())
    
    def __repr__(self):
        return "Lightstatuslog(id='{self.id}',"\
            "light_id='{self.light_id}',"\
            "light_vol='{self.light_vol}',"\
            "light_cur='{self.light_cur}',"\
            "light_pow='{self.light_pow}',"\
            "light_bright='{self.light_bright}',"\
            "envi_bright='{self.envi_bright}',"\
            "temperature='{self.temperature}',"\
            "temperature1='{self.temperature1}',"\
            "temperature2='{self.temperature2}')".format(self=self)


class Warninglog(Base):
    __tablename__ = "warninglogs"

    id = Column(Integer(), primary_key=True)
    light_id = Column(Integer(), ForeignKey('lights.id'))
    status = Column(Integer())
    info = Column(Text())

    def __repr__(self):
        return "Warninglog(id='{self.id}')".format(self=self)


class DataAccessLayer(object):
    def __init__(self):
        self.engine = None
        self.session = None
        self.conn_string = CONN_STRING

    def connect(self):
        self.engine = create_engine(self.conn_string, echo=DEBUG)
        self.Session = sessionmaker(bind=self.engine)


dal = DataAccessLayer()       
        
        
# from sqlalchemy import create_engine
# engine = create_engine('mysql://lanxing:123456@223.3.48.165:3306/gaogandeng', echo=True)
        
# from sqlalchemy.orm import sessionmaker
# Session = sessionmaker(bind=engine)
# session = Session()

