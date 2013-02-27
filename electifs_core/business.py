# Electifs Core - business layer

from .models import *
from .utils import *

_session = None


def get_course (course_id):
    """
    Return one Course with the given id.
    """
    
    return _session.query(Course).filter_by(id=course_id).one()



def get_all_courses (group=False):
    """
    Returns a list of all courses. If group is True, will return a map
    {period: [courses]}, else a list of courses.
    """
    
    courses = _session.query(Course).all()
    
    if group:
        return _group_courses_by_period(courses, True)
    else:
        return courses



def get_courses_by_period (periods, group=False):
    """
    Returns the courses for all the given periods. If group is True, will return
    a map {period: [courses]}, else a list of courses.
    
    periods can be an integer or a list/tuple of integers.
    """
    
    # Ensure that periods is a list of integers between 1 and 12
    periods = to_int_list(periods)
    for i in periods:
        if not ((i >= 1) and (i <= 12)):
            raise ValueError('Period %s is out of bounds' % (i))
    
    # Fetch courses for the requested periods
    courses = _session.query(Course).filter(Course.period.in_(periods)).all()
    
    if group:
        return _group_courses_by_period(courses)
    else:
        return courses



def _group_courses_by_period (courses, all_periods=False):
    """
    Groups a list of Course objects into a dictionnary {period: [courses]}
    
    If all_periods is True, all the periods 1-12 will be added as dictionary keys,
    even if there are no courses in it (value will be an empty list)
    """
    
    courses_dict = {}
    
    if all_periods:
        for i in range(1, 13):
            courses_dict[i] = []
    
    for course in courses:
        if not type(course) is Course:
            raise TypeError('')
        p = course.period
        if not courses_dict.has_key(p):
            courses_dict[p] = []
        courses_dict[p].append(course)
    
    return courses_dict


def get_ratings_for_course (course_id):
    """
    Returns the list of ratings for the given course_id
    """
    
    course_id = int(course_id)
    
    return _session.query(CourseRating).filter_by(course_id=course_id).all()



def count_ratings_for_course (course_id):
    """
    Returns the number of ratings for the given course_id
    """
    
    course_id = int(course_id)
    
    return _session.query(CourseRating).filter_by(course_id=course_id).count()



def get_ratings_for_courses (course_ids=None):
    """
    Return the list of all ratings for the given course_id's, grouped by course
    
    course_ids can be None (will return all ratings), an integer or a list/tuple of integers
    """
    
    # Ensure course_ids is a list of integers
    course_ids = to_int_list(course_ids)
    
    # Prepare query, filter by course_id's if necessary
    q = _session.query(CourseRating)
    if len(course_ids) > 0:
        q = q.filter(CourseRating.course_id.in_(course_ids))
    all_ratings = q.all()
    
    # Group the results by course_id
    grouped_ratings = {}
    for rating in all_ratings:
        cid = rating.course_id
        if not grouped_ratings.has_key(cid):
            grouped_ratings[cid] = []
        grouped_ratings[cid].append(rating)
    
    # Return the grouped results
    return grouped_ratings    



def get_course_average_rating (course_id):
    """
    Computes the average mark (in number of stars) for a course
    """
    
    # Get the ratings
    ratings = get_ratings_for_course(course_id)
    
    # Compute the average
    s = 0
    for rating in ratings:
        s += rating.stars
    
    if s == 0:
        return None
    else:
        return s / len(ratings)


