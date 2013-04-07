# -*- coding: utf-8 -*-

import flask
import json

import config
import electifs_core as core
import json_responses

app = flask.Flask(__name__)


@app.template_filter('default')
def filter_default (s, value):
	if s is None:
		return value
	else:
		return s



@app.route('/', methods=['GET'])
def index ():
	
	session = core.Session()
	
	# Get the list of all courses grouped by period
	courses = core.get_all_courses(session, True)
	
	# For each course, get the number of ratings and the average
	ratings_count = {}
	averages = {}
	for p, period_courses in courses.items():
		for course in period_courses:
			ratings_count[course.id] = core.count_ratings_for_course(session, course.id)
			averages[course.id] = core.get_course_average_rating(session, course.id)
	
	return flask.render_template(
		'index.html',
		courses=courses,
		ratings_count=ratings_count,
		averages=averages
	)



@app.route('/api/ratings', methods=['GET'])
def api_ratings ():
	"""
	Expected URL parameters: course_id
	"""
	
	session = core.Session()
	
	try:
		course_id = flask.request.args.get('course_id')
		
		# Load the course (to check that it exists) and the ratings
		course = core.get_course(session, course_id)
		ratings = core.get_ratings_for_course(session, course_id)
		
		# Return as JSON
		return json_responses.SuccessJsonResponse(
			{ 'ratings': map(core.serialize_rating, ratings) }
		)
	
	except core.exceptions.CourseNotFound:
		flask.abort(404)



@app.route('/api/post-rating', methods=['POST'])
def api_post_rating ():
	"""
	Expected POST body:
	- course_id
	- stars (integer between 0 and 5)
	- remark (text)
	- student_email without @student.ecp.fr suffix
	"""
	
	session = core.Session()
	
	# Validate POST data
	try:
		data = {
			'course_id': flask.request.form['course_id'],
			'stars': flask.request.form['stars'],
			'remark': flask.request.form['remark'],
			'student_email': flask.request.form['student_email'] + core.const.EMAIL_SUFFIX
		}
		# TODO validation (throwing HTTP 400 for errors)
	except Exception:
		return json_responses.BadRequestJsonResponse('validation_failed')
	
	# Check that the course exists, else throw HTTP 412
	try:
		course = core.get_course(session, data['course_id'])
	except core.exceptions.CourseNotFound:
		return json_responses.PreconditionFailedJsonResponse(
			'course_not_found',
			'No course was found with the given course_id.',
			{'course_id': data['course_id']}
		)
	
	# Initialize and persist the rating
	# Throws HTTP 412 if this rating conflicts with another from the same student for this course
	try:
		rating = core.CourseRating(
			course=course,
			stars=data['stars'],
			remark=data['remark'],
			student_email=data['student_email']
		)
		core.save_course_rating(session, rating)
		
	except core.exceptions.ConcurrentRatings:
		return json_responses.PreconditionFailedJsonResponse(
			'concurrent_ratings',
			'Another rating for this course with the same student_email already exists.'
		)
	
	return json_responses.SuccessJsonResponse()



app.run(debug=False)


