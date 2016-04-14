// Import express
var express = require('express');
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);

// Load config for RethinkDB and express
var config = require(__dirname+"/config.js");

var r = require('rethinkdb');

var rdbconn = null;


/*
 * Subscribe to Podium's responses
*/
var podiums_socket = io.of('/podiums');
var active_podiums = [];
podiums_socket.on('connection', function(socket) {
  socket.on('join_podium', function(data) {
    var podium_title = data["podium_title"];
    socket.join(podium_title, function(err) {
      if (err) throw err; 
    });
    if (!(podium_title in active_podiums)) {
      subscribe_to_podium_poll_responses(podium_title)      
      active_podiums.push(podium_title);
    }
  })
})


function polls_podium_join(query, podium_filters) {
  return query.table('polls').eqJoin('podium_id', r.table('podiums'))
      .filter({"right": podium_filters});
}

function get_podium_poll_id(podium_title) {
  podium_filters = {"title": podium_title};
  return r.table('polls').eqJoin('podium_id', r.table('podiums'))
    .filter({"right": podium_filters})
    .pluck({"left": "id"})
    .zip()
    .run(rdbconn)
}

function subscribe_to_podium_poll_responses(podium_title) {
  var poll_change_query = get_podium_poll_id(podium_title)
  .then(function(cursor) {return cursor.toArray()})
  .then(function(result) { 
    var poll_id = result[0]["id"]; 
    return r.table('polls').get(poll_id)
      .changes({includeInitial: true})
      .run(rdbconn);
  })

  poll_change_query
  .then(function(cursor) {
    cursor.each(function(err, changes) {
      if (err) throw err;

      var responses = changes["new_val"]["responses"];
      // sum counts for each response option
      var counts = responses.reduce(function(acc, response) {
        var option = response["option"];
        if (option in acc) {
          acc[option] = acc[option] + 1;
        } else {
          acc[option] = 1;         
        }
        return acc;
      }, {});
      
      podiums_socket.to(podium_title).emit('new_data', counts);
    });
  })
  .then(function(counts) {
    console.log('counts: ', counts);
  })
  .catch(function(err) {
    console.log(err);
  })
}

/*
 * Create a RethinkDB connection, and save it in req._rdbConn
*/
r.connect(config.rethinkdb)
  .then(function(conn) {
    rdbconn = conn;
    startExpress();
  }).error(function(err) {
    throw err;
  });


function startExpress() {
    http.listen(config.express.port);
    console.log('Listening on port '+config.express.port);
}
