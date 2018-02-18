var socket = io()

$('#button').click(function() {
    console.log("Pressed");
    $.ajax({
        type: 'POST',
        url: '/record',
        data: {
            path: "test.webm",
        },
        success: function(data, status) {
        },
    })
});

