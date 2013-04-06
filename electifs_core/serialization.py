"""
Functions for embedding core objects into JSON responses.
"""
from .models import *


def serialize_rating (rating):
    
    if not isinstance(rating, CourseRating):
        raise TypeError("%s is not a CourseRating" % (rating))
    
    return {
        'rating_id': rating.id,
        'course_id': rating.course_id,
        'student_email': rating.student_email,
        'stars': rating.stars,
        'remark': rating.remark,
        'posted_on': rating.posted_on.strftime('%Y-%m-%d %H:%i:%s') if rating.posted_on else None,
        'is_verified': rating.is_verified,
        'is_accepted': rating.is_accepted
    }

