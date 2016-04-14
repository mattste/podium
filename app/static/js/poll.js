
/* Websocket */
var port = 3000
var url = location.protocol + "//" + location.hostname + ":" + port + "/podiums";
var io = io(url);


var podium_title = location.pathname.split("/")[2];
io.emit('join_podium', {"podium_title": podium_title});
io.on('new_data', function(new_data) {
    
    var unload = []
    if (data_state === data_states['fetching_responses']) {
        unload.push(data_states['fetching_responses'])
    } else if (data_state === data_states['no_responses']) {
        unload.push(data_states['no_responses']);
    }
    data_state = data_states['responses_loaded'];
    
    updateChartData(new_data, [data_states['no_responses'], data_states['fetching_responses']])
});
/* End Websocket */

/* Charting */
var data_states = {
    fetching_responses: 'Fetching responses',
    no_responses: 'No poll responses yet',
    responses_loaded: 'Responses loaded'
} 
var initial_data = [[data_states['fetching_responses'], 1]];
var data_state = data_states['fetching_responses'];

var chart = c3.generate({
    bindto: '#chart',
    size: {
        height: 350,
        width: 350
    },
    data: {
        columns: initial_data,
        type : 'donut',
    },
    donut: {
        title: "Latest Poll"
    }
});

// wait specified time to see if the server returns any data
// if no data is returned change the state to be no responses found
setTimeout(function() {
    if (data_state === data_states['fetching_responses']) {
        var new_data = {};
        new_data[data_states['no_responses']] = 1;
        data_state = 'no_responses';
        updateChartData(new_data, [ data_states['fetching_responses'] ]);
    }
}, 2000);

function updateChartData(new_data, unload=[]) {

    var sorted_option_keys = _.sortKeysBy(new_data)
    var columns = _.map(sorted_option_keys, function(option_count, option_key) {
        return [option_key, option_count];
    });

    chart.load({
        columns: columns,
        unload: unload
    })
}
/* End Charting */


/* Underscore util to sort object based on key. Referenced
    from colingourlay at https://gist.github.com/colingourlay/82506396503c05e2bb94
*/
_.mixin({
    'sortKeysBy': function (obj, comparator) {
        var keys = _.sortBy(_.keys(obj), function (key) {
            return comparator ? comparator(obj[key], key) : key;
        });

        return _.zipObject(keys, _.map(keys, function (key) {
            return obj[key];
        }));
    }
});