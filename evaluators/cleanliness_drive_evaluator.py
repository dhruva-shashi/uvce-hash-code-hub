def cleanliness_drive_evaluator(input_file_path, output_file_contents):
	fin = open(input_file_path, 'r')

	points = 0

	try:
		l, b, n, m, k = map(int, fin.readline().split())

		volunteers = []
		for i in range(0, n):
			volunteers.append(list(map(int, fin.readline().split())))

		dustbins = []
		for i in range(0, m):
			dustbins.append(list(map(int, fin.readline().split())))

		landfills = []
		for i in range(0, k):
			landfills.append(list(map(int, fin.readline().split())))

		assignments = list(map(str, output_file_contents.split('\n')))

		while len(assignments) > 0 and assignments[-1] == '':
			assignments.pop()

		if len(assignments) != n:
			raise Exception('N lines not found\n')

		for i in range(0, n):
			temp = assignments[i].split()

			if len(temp) != 2 or (temp[0] != 'D' and temp[0] != 'L'):
				raise Exception('Wrong output format on line %d' % (i+1))

			if temp[0] == 'D' and (int(temp[1]) < 1 or int(temp[1]) > m):
				raise Exception('Wrong index. Dustbin %d does not exist' % (temp[1]))

			if temp[0] == 'L' and (int(temp[1]) < 1 or int(temp[1]) > k):
				raise Exception('Wrong index. Landfill %d does not exist' % (temp[1]))

			assignments[i] = [temp[0], int(temp[1])]

		weights = []
		for i in range(0, m):
			weights.append(0)

		print(assignments, weights, volunteers, dustbins)

		for i in range(0, n):
			if assignments[i][0] == 'D':
				weights[assignments[i][1]-1] += volunteers[i][2]

		for i in range(0, m):
			if weights[i] > dustbins[i][2]:
				raise Exception('Dustbin %d exceeds capacity' % (i+1))

		for i in range(0, n):
			if assignments[i][0] == 'D':
				x = assignments[i][1]-1
				distance = abs(volunteers[i][0]-dustbins[x][0])+abs(volunteers[i][1]-dustbins[x][1])
				points = max(points, distance)

			if assignments[i][0] == 'L':
				x = assignments[i][1]-1
				distance = abs(volunteers[i][0]-landfills[x][0])+abs(volunteers[i][1]-landfills[x][1])
				points = max(points, distance)

		points = l+b-points

	except Exception as e:
		fin.close()

		return {'result': 'WA', 'error': str(e), 'points': 0}

	fin.close()

	return {'result': 'AC', 'points': points}



