from bottle import get, post, route, static_file, template, run, request, default_app

from evaluators.fest_scheduling_evaluator import fest_scheduling_evaluator
from evaluators.network_issue_evaluator import network_issue_evaluator
from evaluators.cleanliness_drive_evaluator import cleanliness_drive_evaluator
from evaluators.book_scanning_evaluator import book_scanning_evaluator

from problem import htmlize_problem

import json
import os


f = open('problems.json', 'r')
problems = json.load(f)
f.close()


@route('/')
def index():
	return template('front-end/templates/index.html')


@route('/styles/<filename>.css')
def styles(filename):
	return static_file('front-end/styles/'+filename+'.css', root='.')


@route('/scripts/<filename>.js')
def scripts(filename):
	return static_file('front-end/scripts/'+filename+'.js', root='.')


@route('/input-file/<problem>/<filename>.txt')
def scripts(problem, filename):
	print('input-files/'+problem+'/'+filename+'.txt')
	return static_file('input-files/'+problem+'/'+filename+'.txt', root='.')


@route('/problem-statement/<problem>.pdf')
def problem_statement(problem):
	return static_file('/problem-statements/%s.pdf' % (problem), root='.')


@route('/problems/<problem>')
def get_problem(problem):
    return htmlize_problem(problem)


@route('/images/icon')
def get_icon():
	return static_file('front-end/images/icon.jpg', root='.')


@route('/images/telegram')
def get_telegram_icon():
	return static_file('front-end/images/telegram.png', root='.')


@route('/images/email')
def get_telegram_icon():
	return static_file('front-end/images/email.png', root='.')


@get('/cookie-init')
def cookie_init():
	result = {}

	for problem in problems:
		temp = []

		for i in range(0, problems[problem]['number-of-inputs']):
			temp.append(0)

		result[problem] = temp

	return result


@post('/submission/<problem>')
def submission(problem):
	if problem not in problems:
		return {'error': 'Problem does not exist'}

	files = list()

	number_of_files = 0

	for i in range(1, problems[problem]['number-of-inputs']+1):
		files.append(request.files.get('file%d' % i))
		if files[-1]:
			number_of_files += 1

    # If the number of output files is 0, do not evaluate the submission
	if number_of_files == 0:
		return {'error': 'No output files found'}

	score = []

	for i in range(0, problems[problem]['number-of-inputs']):
		if not files[i]:
			score.append({'result': 'NF', 'points': 0})
		else:
			# Initialize the path for input file
			input_file_path = 'input-files/%s/input-%s.txt' % (problem, chr(i+ord('a')))

			# Initialize the path for output file and save the output file temporarily
			output_file_content = files[i].file.read().decode()

			if problem == 'fest-scheduling':
				score.append(fest_scheduling_evaluator(input_file_path, output_file_content))
			elif problem == 'network-issue':
				score.append(network_issue_evaluator(input_file_path, output_file_content))
			elif problem == 'cleanliness-drive':
				score.append(cleanliness_drive_evaluator(input_file_path, output_file_content))
			elif problem == 'book-scanning-2020-qualification':
				score.append(book_scanning_evaluator(input_file_path, output_file_content))

	return {'ok': True, 'scores': score}

app = default_app()


