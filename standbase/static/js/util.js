function getRandomArbitrary(min, max) {
	return Math.random() * (max - min) + min;
}

/*
 * Takes a duration in seconds and returns parts depending on the 
 * units of time you can fill with them.
 */
function listDuration(d) {
	var days = Math.floor(d / (24 * 60 * 60));
	d -= days * 24 * 60 * 60;

	var hours = Math.floor(d / (60 * 60));
	d -= hours * 60 * 60;

	var minutes = Math.floor(d / 60);
	d -= minutes * 60;

	var seconds = d;

	var returnValue = [];

	if (days > 1) {
		returnValue.push(days + " days");
	} else if (days == 1) {
		returnValue.push("1 day");
	}

	if (hours > 1) {
		returnValue.push(hours + ' hours');
	} else if (days == 1) {
		returnValue.push('1 hour');
	}

	if (minutes > 1) {
		returnValue.push(minutes + ' minutes');
	} else if (minutes == 1) {
		returnValue.push('1 minute');
	}

	if (seconds > 1) {
		returnValue.push(seconds + ' seconds');
	} else if (seconds == 1) {
		returnValue.push('1 second');
	}

	return returnValue;
}

/*
 * Formats a set of time parts into a coherent duration.
 */
function formatDuration(d) {
	var items = listDuration(d);

	var returnParts = [];

	for (var i = 0; i < items.length; i++) {
		returnParts.push(items[i]);

		if (i < items.length-2) {
			returnParts.push(', ');
		} else if (i < items.length-1) {
			returnParts.push(' and ');
		}
	}

	return returnParts.join('');
}