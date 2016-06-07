//var surveyJSON = {
//    title: "Tell us, what technologies do you use?", pages: [
//        {
//            name: "page1", questions: [
//            {
//                type: "radiogroup",
//                choices: ["Yes", "No"],
//                isRequired: true,
//                name: "frameworkUsing",
//                title: "Do you use any front-end framework like Bootstrap?"
//            },
//            {
//                type: "checkbox",
//                choices: ["Bootstrap", "Foundation"],
//                hasOther: true,
//                isRequired: true,
//                name: "framework",
//                title: "What front-end framework do you use?",
//                visible: false
//            }
//        ]
//        },
//        {
//            name: "page2", questions: [
//            {
//                type: "radiogroup",
//                choices: ["Yes", "No"],
//                isRequired: true,
//                name: "mvvmUsing",
//                title: "Do you use any MVVM framework?"
//            },
//            {
//                type: "checkbox",
//                choices: ["AngularJS", "KnockoutJS", "React"],
//                hasOther: true,
//                isRequired: true,
//                name: "mvvm",
//                title: "What MVVM framework do you use?",
//                visible: false
//            }]
//        },
//        {
//            name: "page3", questions: [
//            {type: "comment", name: "about", title: "Please tell us about your main requirements for Survey library"}]
//        }
//    ],
//    triggers: [
//        {type: "visible", operator: "equal", value: "Yes", name: "frameworkUsing", questions: ["framework"]},
//        {type: "visible", operator: "equal", value: "Yes", name: "mvvmUsing", questions: ["mvvm"]}
//    ]
//};
//ReactDOM.render(
//    <ReactSurvey json={surveyJSON} onComplete={function(){}}/>,
//    document.getElementById("surveyContainer"));

define(function (require) {
    var JSON5 = require('json5');
});

var jsonResponse,
    jsonData,
    json;

var send = function (survey) {
    console.log(survey);
	var resultAsString = JSON.stringify(survey.data);
	alert(resultAsString); //send Ajax request to your web server.
};

fetch("http://128.199.51.34/api/v1/poll/1/")
    .then((response) => response.text())
    .then((responseText) => {
        jsonResponse = JSON5.parse(responseText);
        jsonData = JSON5.parse(jsonResponse.data);
        json = JSON5.parse(jsonData.json);
        console.log(json);

        ReactDOM.render(
            <ReactSurvey json={json} onComplete={send}/>,
            document.getElementById("surveyContainer"));
    });

