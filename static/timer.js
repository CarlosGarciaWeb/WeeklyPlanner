
var parameters = {}
location.search.slice(1).split("&").forEach( function(key_value) { var kv = key_value.split("="); parameters[kv[0]] = kv[1]; })

var valueHour = parameters['totalHours'];

var timeStarted = parameters['timeStarted']


function startCounter() {
    var totalSeconds = valueHour * 60 * 60;
    var hour = valueHour - 1;
    var minute = 59;
    var second = 60;
    var counterSecs = 0;
    var counterMins = 0;
    var hours = 0;
    var minutes = 0;
    var seconds = 0;
    const interval = setInterval(() => {
        if (totalSeconds < 1) {
            timeStarted = false;
            clearInterval(interval);
        }

        if (counterSecs === 60 && minute >= 0 && totalSeconds > 0) {
            counterMins = counterMins + 1;
            minute = minute - 1;
            counterSecs = 0;
            second = 60;

            if (counterMins == 60) {
                if (hour > 0) {
                    hour = hour - 1;
                    minute = 59;
                }
                counterMins = 0;
            }

        }

        hours = "0" + hour;

        if (second > 9) {
            seconds = second;
        } else {
            seconds = "0" + second;
        }

        if (minute > 9) {
            minutes = minute;
        } else {
            minutes = "0" + minute;
        }
        second = second - 1;
        counterSecs = counterSecs + 1;
        totalSeconds = totalSeconds - 1;
        postMessage([hours+":"+minutes+":"+seconds, timeStarted]);
    }, 1000)
}

startCounter();
