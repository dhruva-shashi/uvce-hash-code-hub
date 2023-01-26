import json


def htmlize_problem(problem):
	f = open('problems.json', 'r')
	problems = json.load(f)
	f.close()

	if problem not in problems:
		return 'Problem does not exist'

	problem_name = problems[problem]['problem-name']
	number_of_inputs = problems[problem]['number-of-inputs']

	html_content = '''
<html>
    <head>
        <title>%s</title>
        <link rel="stylesheet" href="/styles/problem.css">
        <script src="/scripts/problem.js"></script>
    </head>

    <body>
        <div class="heading1"><a href="/" class="heading1">UVCE Hash Code Hub</a></div>
        <div class="heading1">%s</div>

        <div id="container">
            <div id="left-pane">
                <table>
                    <tr>
                        <td>
                            <strong>Downloads</strong>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <a href="/problem-statement/%s.pdf" download>Problem Statement</a>
                        </td>
                    </tr>
	''' % (problem_name, problem_name, problem)

	for i in range(0, number_of_inputs):
		html_content += '''
                    <tr>
                        <td>
                            <a href="/input-file/%s/input-%s.txt" download>Input %s</a>
                        </td>
                    </tr>
		''' % (problem, chr(i+ord('a')), chr(i+ord('A')))

	html_content += '''
                </table>
            </div>

            <div id="right-pane">
                <form id="submission">
                    <table>
                        <tr>
                            <td></td>
                            <td></td>
                            <td><div>Points</div></td>
                            <td><div>Best Points</div></td>
                        </tr>
	'''

	for i in range(0, number_of_inputs):
		html_content += '''
                        <tr>
                            <td>Select file %s</td>
                            <td><input type="file" id="file%d" name="file%d" accept=".txt" /></td>
                            <td><div class="points" id="points-%d">0</div></td>
                            <td><div class="points" id="best-points-%d">0</div></td>
                        </tr>
		''' % (chr(i+ord('A')), i+1, i+1, i+1, i+1)

	html_content += '''
                        <tr>
                            <td>----------------</td>
                            <td>----------------</td>
                            <td>----------------</td>
                            <td>----------------</td>
                        </tr>
                        <tr>
                            <td><strong>Total Points</strong></td>
                            <td> </td>
                            <td><div class="points" id="total-points">0</div></td>
                            <td><div class="points" id="best-total-points">0</div></td>
                        </tr>
                    </table>
                </form>
                <input type="submit" value="Submit" id="submit" onclick="make_submission('%s')"/> <br>
            </div>
        </div>

        <script>
            init("%s");
        </script>
    </body>
</html>
	''' % (problem, problem)

	return html_content

