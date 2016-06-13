define(function (require) {
    var JSON5 = require('json5');
});

var jsonResponse,
    jsonData,
    json;

fetch("http://127.0.0.1:8000/api/v1/get_csrf_token/")
    .then((response) => console.log(response));

var send = function (survey) {
    console.log(survey);

    fetch("http://127.0.0.1:8000/api/v1/poll/", {
        method: 'post',
        credentials: "include",
        headers: {
            "Content-type": "application/json; charset=utf-8",
            "X-CSRFToken": "Q3mX84SS0MiCpoXFJCP1OgIlBGaf0y8z"
        },
        body: survey
    });
    //console.log(survey);
	//var resultAsString = JSON.stringify(survey.data);
	//alert(resultAsString); //send Ajax request to your web server.
};


fetch("http://127.0.0.1:8000/api/v1/poll/1/", {credentials: "include"})
    .then((response) => response.text())
    .then((responseText) => {
        jsonResponse = JSON5.parse(responseText);
        jsonData = JSON5.parse(jsonResponse.data);
        json = JSON5.parse(jsonData.json);


        ReactDOM.render(
            <ReactSurvey json={json} onComplete={send}/>,
            document.getElementById("surveyContainer"));
    });

