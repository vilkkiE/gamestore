
$(document).ready(function() {

  var game_id = $("#user-div").attr("data-game_id");
  $.ajax({
    type: "GET",
    url: "/update_score/",
    data: {
      "game_id": game_id,
      "csrfmiddlewaretoken" : $("input[name=csrfmiddlewaretoken]").val()
    },
    success: updateHighscores,
    dataType: "json"
  });
  window.addEventListener("message", receiveMessage, false);
});

/**
*   Method that updates the Highscore list shown to players with the given data
*/
function updateHighscores(data){
  var d = data;
  console.log(data);
  var user_scores = data.user_scores;
  delete data.user_scores;
  console.log(user_scores);
  console.log(data);
  var scores = [];
  for (var score in d){
    scores.push([d[score][0],d[score][1]]);
  }
  scores = scores.sort(function(a, b){return b[1]-a [1];});
  var global_html="";
  for (var s in scores){
    s = scores[s];
    global_html += "<li>"+s[0]+": "+s[1]+"</li>\n";
  }
  var user_html="";
  for (var i in user_scores){
    user_html += "<li>"+user_scores[i]+"</li>\n";
  }
  $("#user_highscores").html(user_html);
  $("#highscores").html(global_html);
}


/**
*   Method that loads the given save data into the game
*/
function loadSave(data){
  var payload = data;
  if (data["messageType"] === "LOAD"){
    data["gameState"] = JSON.parse(data["gameState"]);
    $("#game-status").html("<p>Game Loaded</p>");
  }
  var gameWindow = document.getElementById("gamewindow").contentWindow;
  gameWindow.postMessage(payload, "*");
}

/**
*   Method is used to listen to events sent from the game iframe. Available
*   events are "SCORE", "SAVE", "LOAD_REQUEST" and "SETTING"
*/
function receiveMessage(event) {
  var origin = event.origin || event.originalEvent.origin;
  var originLength = origin.length;
  var gamesource = $("#gamewindow").attr("src");
  var user_id = $("#user-div").attr("data-user_id");
  var game_id = $("#user-div").attr("data-game_id");
  gamesource = gamesource.substring(0,originLength);
  if (origin !== gamesource) {
    return;
  }
  var messageType = event.data.messageType;
  if (messageType === "SCORE") {
    var score = event.data.score;
    $("#game-status").html("<p>Score Saved</p>");
    $.ajax({
      type: "POST",
      url: "/update_score/",
      data: {
        "score": score.toString(),
        "user_id": user_id,
        "csrfmiddlewaretoken" : $("input[name=csrfmiddlewaretoken]").val(),
        "game_id": game_id,
      },
      success: updateHighscores,
      dataType: "json"
    });

  } else if (messageType === "SAVE") {
    var gameState = event.data.gameState;
    $("#game-status").html("<p>Game Saved</p>");
    $.ajax({
      type: "POST",
      url: "/save_game/",
      data: {
        "save_data": JSON.stringify(gameState),
        "game_id": game_id,
        "user_id": user_id,
        "csrfmiddlewaretoken" : $("input[name=csrfmiddlewaretoken]").val()
      }
    });
  } else if (messageType === "LOAD_REQUEST") {
    $.ajax({
      type: "GET",
      url: "/load_game/",
      data:{
        "user_id": user_id,
        "game_id": game_id,
        "csrfmiddlewaretoken" : $("input[name=csrfmiddlewaretoken]").val()
      },
      success: loadSave,
      dataType: "json"
    });
  } else if (messageType === "SETTING"){
    var settings = event.data.options;
    $("#iframe-div").attr("class","game-setting");
    $("#iframe-div").css("padding-bottom","0%");
    $("#gamewindow").attr("width", settings["width"]);
    $("#gamewindow").attr("height", settings["height"]);
  }
}
