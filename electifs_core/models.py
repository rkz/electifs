# Electifs Core - model layer

import sqlalchemy
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

import datetime

Base = declarative_base()



class Course(Base):
    id = Column('course_id', Integer, primary_key=True)
    name = Column(String(60))
    teacher_name = Column(String(60))
    period = Column(Integer)
    is_available = Column(Boolean)
    
    #ratings = relationship('CourseRating', backref='course')
    
    __tablename__ = 'course'
    
    def __repr__ (self):
        return '<Course #%s %s>' % (self.id, self.name)



class CourseRating(Base):
    id = Column('course_rating_id', Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('course.course_id'))
    student_email = Column(String(60))
    posted_on = Column(DateTime)
    stars = Column(Integer)
    remark = Column(Text)
    is_verified = Column(Boolean)  # e-mail verified
    is_accepted = Column(Boolean)  # rating accepted by moderators
    
    course = relationship('Course', backref=backref('course_rating', order_by=id))
    
    __tablename__ = 'course_rating'
    
    def __init__ (self, **kwargs):
        """
        Convenience constructor for creating new CourseRating's. Accepted keyword
        arguments are course, student_email, stars and remark. posted_on will be
        set to the current date, is_verified and is_accepted will be initialized 
        to False.
        
        PROBLEM: how to validate this input data? (should be in business layer... ???)
        """
        
        for arg in ('course', 'student_email', 'remark', 'stars'):
            if kwargs.has_key(arg):
                setattr(self, arg, kwargs[arg])
        
        self.posted_on = datetime.datetime.now()
        self.is_verified = False
        self.is_accepted = False
    
    
    def __repr__ (self):
        return '<CourseRating #%d by %s for course %s>' % (self.id, self.student_email, self.course_id)


