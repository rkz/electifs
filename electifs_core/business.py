# Electifs Core - business layer

from .models import *
from .utils import *
import const
import exceptions as core_exc
import sqlalchemy.orm.exc as sqla_exc
from sqlalchemy.orm.util import has_identity


def get_course (session, course_id):
    """
    Return one Course with the given id.
    """
    
    try:
        return session.query(Course).filter_by(id=course_id).one()
    except sqla_exc.NoResultFound:
        raise core_exc.CourseNotFound(course_id)
    except:
        raise core_exc.UnexpectedResult



def get_all_courses (session, group=False):
    """
    Returns a list of all courses. If group is True, will return a map
    {period: [courses]}, else a list of courses.
    """
    
    courses = session.query(Course).all()
    
    if group:
        return _group_courses_by_period(session, courses, True)
    else:
        return courses



def get_courses_by_period (session, periods, group=False):
    """
    Returns the courses for all the given periods. If group is True, will return
    a map {period: [courses]}, else a list of courses.
    
    periods must be a list/tuple of integers.
    """
    
    # Ensure that all the periods are within the bounds
    for i in periods:
        if not ((i >= const.periods.MIN) and (i <= const.periods.MAX)):
            raise ValueError('Period %s is out of bounds' % (i))
    
    # Fetch courses for the requested periods
    courses = session.query(Course).filter(Course.period.in_(periods)).all()
    
    if group:
        return _group_courses_by_period(session, courses)
    else:
        return courses



def _group_courses_by_period (session, courses, all_periods=False):
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


def get_ratings_for_course (session, course_id, active_ratings=True):
    """
    Returns the list of ratings for the given course_id
    """
    
    course_id = int(course_id)
    
    q = session.query(CourseRating).filter_by(course_id=course_id)
    if active_ratings:
        q = q.filter_by(is_verified=True).filter_by(is_verified=True)
    return q.all()



def count_ratings_for_course (session, course_id, active_ratings=True):
    """
    Returns the number of ratings for the given course_id
    """
    
    course_id = int(course_id)
    
    q = session.query(CourseRating).filter_by(course_id=course_id)
    if active_ratings:
        q = q.filter_by(is_verified=True).filter_by(is_verified=True)
    return q.count()



def get_ratings_for_courses (session, course_ids=None):
    """
    Return the list of all ratings for the given course_id's, grouped by course
    
    course_ids can be None (will return all ratings), an integer or a list/tuple of integers
    """
    
    # Ensure course_ids is a list of integers
    course_ids = to_int_list(course_ids)
    
    # Prepare query, filter by course_id's if necessary
    q = session.query(CourseRating)
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



def get_course_average_rating (session, course_id):
    """
    Computes the average mark (in number of stars) for a course
    """
    
    # Get the ratings
    ratings = get_ratings_for_course(session, course_id)
    
    # Compute the average
    s = 0
    for rating in ratings:
        s += rating.stars
    
    if len(ratings) == 0:
        return None
    else:
        return s / len(ratings)



def save_course_rating (session, rating):
    """
    Saves a course rating.
    If the rating has not been persisted yet, checks that there is
    no other rating for this course from this student ("concurrent ratings")
    """
    
    # TODO validate rating object
    
    # Check that there are no concurrent ratings
    # (If the object is persisted, this check has already been made and is
    # therefore no longer needed)
    if rating.id is None: # not persisted yet
        q = session.query(CourseRating)\
              .filter(CourseRating.course_id == rating.course.id)\
              .filter(CourseRating.student_email == rating.student_email)
        if q.count() > 1:  # includes current course
            raise core_exc.ConcurrentRatings(rating.course, rating.student_email)
    
    # Persist rating    
    session.add(rating)
    session.commit()

