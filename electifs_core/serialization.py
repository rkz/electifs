from .models import *


def serialize_rating (rating):
    
    if not isinstance(rating, CourseRating):
        raise TypeError("%s is not a CourseRating" % (rating))
    
    return {
        'rating_id': rating.id,
        'course_id': rating.course_id,
        'student_email': rating.student_email,
        'student_promotion': rating.student_promotion,
        'stars': rating.stars,
        'remark': rating.remark
    }

