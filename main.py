from bottle import get, post, run, route, request, static_file, template
from fest_scheduling_evaluator import fest_scheduling_evaluator
from network_issue_evaluator import network_issue_evaluator
from cleanliness_drive_evaluator import cleanliness_drive_evaluator
from problem import htmlize_problem
import json
import os


f = open('problems.json', 'r')
problems = json.load(f)
f.close()


@route('/')
def index():
	return template('index.html')


@route('/styles/<filename>.css')
def styles(filename):
	return static_file(filename+'.css', '.')


@route('/scripts/<filename>.js')
def scripts(filename):
	return static_file(filename+'.js', '.')


@route('/problem-statement/<problem>.pdf')
def problem_statement(problem):
	return static_file('/problem-statements/%s.pdf' % (problem), '.')


@route('/input-file/<problem>/<filename>.txt')
def problem_statement(problem, filename):
	return static_file('/input-files/%s/%s.txt' % (problem, filename), '.')


@route('/problems/<problem>')
def get_problem(problem):
    return htmlize_problem(problem)


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
		if files[i-1]:
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
			output_file_path = 'output-%s.txt' % (chr(i+ord('a')))
			files[i].save(output_file_path)

			if problem == 'fest-scheduling':
				score.append(fest_scheduling_evaluator(input_file_path, output_file_path))
			elif problem == 'network-issue':
				score.append(network_issue_evaluator(input_file_path, output_file_path))
			elif problem == 'cleanliness-drive':
				score.append(cleanliness_drive_evaluator(input_file_path, output_file_path))

			os.remove(output_file_path)

	return {'ok': True, 'scores': score}


if os.environ.get('APP_LOCATION') == 'heroku':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    run(host='localhost', port=8080, debug=True)

