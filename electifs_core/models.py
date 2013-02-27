# Electifs Core - model layer

import sqlalchemy

from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

################################################################################


class Course(Base):
    id = Column('course_id', Integer, primary_key=True)
    name = Column(String(60))
    teacher_name = Column(String(60))
    period = Column(Integer)
    is_available = Column(Boolean)
    
    #ratings = relationship('CourseRating', backref='course')
    
    __tablename__ = 'course'
    
    def __repr__ (self):
        return '<Course %s>' % (self.id)

################################################################################


class CourseRating(Base):
    id = Column('course_rating_id', Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('course.course_id'))
    student_email = Column(String(60))
    student_promotion = Column(Integer)
    stars = Column(Integer)
    remark = Column(Text)
    
    course = relationship('Course', backref=backref('course_rating', order_by=id))
    
    __tablename__ = 'course_rating'
    
    def __repr__ (self):
        return '<CourseRating for course %s>' % (self.course_id)

################################################################################

