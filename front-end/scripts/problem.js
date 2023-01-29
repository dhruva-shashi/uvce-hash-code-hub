function init(problem) {
	if (document.cookie == '') {
		var xmlHttp = new XMLHttpRequest();
		xmlHttp.open("GET", '/cookie-init-all', false);
		xmlHttp.send(null);

		document.cookie = "problem-scores="+xmlHttp.responseText+"; expires=Tue, 31 Dec 2030 23:59:59 UTC";
	}

	var problem_scores = JSON.parse(document.cookie.split(';')[0].split('=')[1]);

	if (!(problem in problem_scores)) {
		var xmlHttp = new XMLHttpRequest();
		xmlHttp.open("GET", `/cookie-init/${problem}`, false);
		xmlHttp.send(null);

		problem_scores[problem] = JSON.parse(xmlHttp.responseText);

		document.cookie = "problem-scores="+JSON.stringify(problem_scores)+"; expires=Tue, 31 Dec 2030 23:59:59 UTC";
	}

	var total_points = 0;

	for (var i = 0; i < problem_scores[problem].length; i++) {
		document.getElementById('best-points-'+(i+1)).innerHTML = problem_scores[problem][i];
		total_points += problem_scores[problem][i];
	}

	document.getElementById('best-total-points').innerHTML = total_points;
}

function make_submission(problem) {
    var number_of_empty_files = 0;

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/submission/"+problem);

    xhr.onload = function(event) {
        if ('error' in JSON.parse(event.target.response)) {
            alert(JSON.parse(event.target.response)['error']);
            return ;
        }

		var best_scores = JSON.parse(document.cookie.split(';')[0].split('=')[1]);

		var total_points = 0;
		var best_total_points = 0;

		var scores = JSON.parse(event.target.response)['scores'];

		var alert_message = '';

		for (var i = 0; i < best_scores[problem].length; i++) {
			if ('error' in scores[i])
				alert_message += 'Output '+String.fromCharCode(65+i)+': '+scores[i]['error']+'\n';

			if (scores[i]['points'] > best_scores[problem][i])
				best_scores[problem][i] = scores[i]['points'];

			document.getElementById('points-'+(i+1)).innerHTML = scores[i]['points'];
			document.getElementById('best-points-'+(i+1)).innerHTML = best_scores[problem][i];

			total_points += scores[i]['points'];
			best_total_points += best_scores[problem][i];
		}

		if (alert_message != '')
			alert(alert_message);

		document.getElementById('total-points').innerHTML = total_points;
		document.getElementById('best-total-points').innerHTML = best_total_points;
		
		document.cookie = "problem-scores="+JSON.stringify(best_scores)+"; expires=Tue, 31 Dec 2030 23:59:59 UTC";
    };

    var formData = new FormData(document.getElementById("submission"));

    xhr.send(formData);

    document.getElementById('submission').reset();
}


