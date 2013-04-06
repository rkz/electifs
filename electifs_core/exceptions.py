# Business layer exceptions

# Global exceptions

class CoreException (Exception):
    pass

class NotFound (CoreException):
    pass

class MultipleResultsFound (CoreException):
    pass

class UnexpectedResult (CoreException):
    pass


# Model-specific exceptions

class CourseNotFound (NotFound):
    def __init__ (self, course_id):
        self.course_id = course_id



class ConcurrentRatings (CoreException):
    def __init__ (self, course, student_email):
        self.course = course
        self.student_email = student_email