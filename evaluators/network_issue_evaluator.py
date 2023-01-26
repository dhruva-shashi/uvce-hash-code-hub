def network_issue_evaluator(input_file_path, output_file_contents):
	fin = open(input_file_path, 'r')

	points = 0

	try:
		n, m = map(int, fin.readline().split())

		teams = []
		for i in range(0, n):
			teams.append(list(map(int, fin.readline().split())))

		locations = []
		for i in range(0, m):
			locations.append(list(map(int, fin.readline().split())))

		total_individuals = []
		for i in range(0, m):
			total_individuals.append(0)

		assignments = list(map(str, output_file_contents.split('\n')))
		while len(assignments) > m and assignments[-1] == '':
			assignments.pop()

		for i in range(0, m):
			assignments[i] = list(map(int, assignments[i].split()))

		s = set()

		for i in range(0, m):
			for j in assignments[i]:
				if j < 1 or j > n:
					raise Exception('Wrong index. Team %d does not exist' % (j))
				else:
					s.add(j)

		if len(s) != n:
			raise Exception('Not all teams have been assigned locations')

		for i in range(0, m):
			for j in assignments[i]:
				total_individuals[i] += teams[j-1][0]

		final_bandwidths = []

		for i in range(0, m):
			final_bandwidths.append(locations[i][0]-(locations[i][1]*(total_individuals[i]//locations[i][2])))

		for i in range(0, m):
			for j in assignments[i]:
				if final_bandwidths[i] >= teams[j-1][1]:
					points += teams[j-1][0]

	except Exception as e:
		fin.close()

		return {'result': 'WA', 'error': str(e), 'points': 0}

	fin.close()

	return {'result': 'AC', 'points': points}
	
