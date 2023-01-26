def fest_scheduling_evaluator(input_file_path, output_file_contents):
	fin = open(input_file_path, 'r')

	points = 0

	try:
		n, m, k = map(int, fin.readline().split())

		tags = []
		for i in range(0, n*m):
			tags.append(list(map(str, fin.readline().split())))

		assignments = output_file_contents.split('\n')

		while len(assignments) > 0 and assignments[0] == '':
			assignments.pop(0)

		while len(assignments) > 0 and assignments[-1] == '':
			assignments.pop()

		if len(assignments) != n:
			raise Exception('N lines not present in output')

		for i in range(0, n):
			assignments[i] = list(map(int, assignments[i].split()))

			if len(assignments[i]) != m:
				raise Exception('M integers not present in line %d' % (i+1))

		for i in range(0, n):
			for j in range(0, m):
				if assignments[i][j] < 1 or assignments[i][j] > n*m:
					raise Exception('Wrong index. Event %d not present' % (assignments[i][j]))

		for i in range(0, n):
			s = set()

			for j in range(0, m):
				for x in range(0, k):
					s.add(tags[assignments[i][j]-1][x])

			points += len(s)

	except Exception as e:
		fin.close()

		return {'result': 'WA', 'error': str(e), 'points': 0}

	fin.close()

	return {'result': 'AC', 'points': points}
	
