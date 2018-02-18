var express = require('express')
var app = express()
var bodyParser = require('body-parser')
var exphbs = require('express-handlebars')
var mongoose = require('mongoose')
var dotenv = require('dotenv')
var schedule = require('node-schedule')
var Analysis = require('./models/Analysis')
var request = require('request')
var PythonShell = require('python-shell');
var pyshell = new PythonShell('/python/frames.py');

dotenv.load()

app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: false }))
app.use('/public', express.static('public'))
app.engine('handlebars', exphbs({ defaultLayout: 'main' }))
app.set('view engine', 'handlebars')

mongoose.connect(process.env.MONGODB)
mongoose.connection.on('error', function() {
    console.log(
        'MongoDB Connection Error. Please make sure that MongoDB is running.',
    )
    process.exit(1)
})

var http = require('http').Server(app)
var io = require('socket.io')(http)

app.get('/', function(req, res) {
    res.render('home',{});

});

app.get('/record', function(req, res) {
    console.log("Homepage");
    console.log("WERE HERE");
    res.render('home',{});
});

app.post('/record', function(req, res) {
  var url = req.body.url;
  pyshell.on('message', function(message){
    console.log(message)
  }
);

PythonShell.run('/python/frames.py', function(err, data){
    if (err){
        console.log(err);
    } else {
        var jsonData = JSON.parse(data);
        console.log(jsonData);
        for (var i in jsonData) {
            var analysis = new Analysis ({
              time: jsonData[i].time,
              text: jsonData[i].text,
              expression: jsonData[i].expression,
              keywords: jsonData[i].keywords,
              sentiment: jsonData[i].sentiment
              //roll: jsonData[i].roll,
              //pitch: jsonData[i].pitch,
              //yaw: jsonData[i].yaw,

          });
            analysis.save(function(err){
              if (err){
                console.log(err);
              } else {
                  console.log("successfully saved");
              }
            });
          }
    }}); 
});

http.listen(3000, function() {
    console.log('Example app listening on port 3000!')
});
