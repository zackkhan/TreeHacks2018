var mongoose = require('mongoose');

var AnalysisSchema = new mongoose.Schema({
    time: {
        type: Number,
        required: false
    },
    text: {
        type: String,
        required: false
    },
   volume: {
        type: Number,
        required: false
    },
    expression: {
        type: String, 
        required: false
    },
    yaw: {
        type: Number,
        required: false
    },
    roll: {
        type: Number,
        required: false
    },
    pitch: {
        type: Number,
        required: false
    },
    keywords: {
        type: [String], 
        required: false
    },
    sentiment: {
        type: Number,
        required: false
    }
});


var Analysis = mongoose.model('Analysis', AnalysisSchema);

module.exports = Analysis;