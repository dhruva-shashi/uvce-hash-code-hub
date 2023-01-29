import heapq

def book_scanning_evaluator(input_file_path, output_file_contents):
	fin = open(input_file_path, 'r')

	points = 0

	try:
		'''
			Variables:

			b [int]					Number of books 
			l [int]					Number of libraries
			d [int]					Number of days

			m [int]					Number of registered libraries

			book_score [list]		The number of points awarded for shipping the ith book

			library_info [list]		Two lists -	1. Contains the number of books, Signup process time, Number of books which can be shipped in a day
												2. Id of each book available in that library
		'''

		b, l, d = map(int, fin.readline().split())

		book_score = list(map(int, fin.readline().split()))

		library_info = []

		for i in range(0, l):
			library_info.append([])
			library_info[i].append(list(map(int, fin.readline().split())))
			library_info[i].append(set(map(int, fin.readline().split())))

		assignments = output_file_contents.split('\n')

		while len(assignments) > 0 and assignments[0] == '':
			assignments.pop(0)

		while len(assignments) > 0 and assignments[-1] == '':
			assignments.pop()

		m = int(assignments[0])
		assignments.pop(0)

		if len(assignments) != 2*m:
			raise Exception('2*A lines not present in output')

		for i in range(0, m):
			assignments[2*i] = list(map(int, assignments[2*i].split()))
			assignments[(2*i)+1] = list(map(int, assignments[(2*i)+1].split()))

		time_gone = 0

		for i in range(0, m):
			y, k = assignments[0][0], assignments[0][1]
			assignments.pop(0)

			a = assignments[0]
			assignments.pop(0)

			if len(a) != k:
				raise Exception('Not enough books for library %d' % y)

			if len(set(a)) != k:
				raise Exception('Duplicate books while scanning library %d' % y)

			time_gone += library_info[y][0][1]

			for j in range(0, k):
				if a[j] in library_info[y][1] and time_gone+(j/library_info[y][0][2]) < d:
					points += book_score[a[j]]
					book_score[a[j]] = 0

	except Exception as e:
		fin.close()

		return {'result': 'WA', 'error': str(e), 'points': 0}

	fin.close()

	return {'result': 'AC', 'points': points}
	
