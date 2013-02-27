# -*- coding: utf-8 -*-

import flask
import json
import config

import electifs_core as core

app = flask.Flask(__name__)


@app.template_filter('default')
def filter_default (s, value):
	if s is None:
		return value
	else:
		return s



@app.route('/')
def index ():
	
	# Get the list of all courses grouped by period
	courses = core.get_all_courses(True)
	
	# For each course, get the number of ratings and the average
	ratings_count = {}
	averages = {}
	for p, period_courses in courses.items():
		for course in period_courses:
			ratings_count[course.id] = core.count_ratings_for_course(course.id)
			averages[course.id] = core.get_course_average_rating(course.id)
	
	return flask.render_template('index.html',
		courses=courses,
		ratings_count=ratings_count,
		averages=averages
	)



@app.route('/api/ratings') # expects course_id as URL parameter
def api_ratings ():
	
	# Cast URL parameter course_id to integer
	try:
		course_id = int(flask.request.args.get('course_id'))
	except:
		flask.abort(400) # bad request
	
	# Get the list of ratings for this course
	ratings = core.get_ratings_for_course(course_id)
	
	# Return as JSON
	return json.dumps(ratings, default=core.serialize_rating)



app.run(debug=True)

