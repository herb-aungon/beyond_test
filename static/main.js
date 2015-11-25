var url = "http://herbportal.ddns.net/"
var token_id = 0;
var user = 0;
var message = 0;
var success = 0;

$("#login_").click(function() {
    var username = $('#username').val();
    var password = $('#password').val();

    var user = {};
    user["username"] = username;
    user["password"] = password;
    var json_user= JSON.stringify(user);
    console.log(json_user);    
    $.ajax({
    	type : "POST",
    	url : url + "beyond_login",
    	data: json_user,
    	contentType: 'application/json;charset=UTF-8',
    	headers: {
    	    'X-token':'',
    	    'Content-Type':'application/json'
    	},
    	success: function(result) {
    	    console.log(result);
    	    result_ = JSON.parse(result);
    	    token_id = result_['data'];

    	},
    	async: false
    });
    console.log(token_id);
    if(token_id){
    	console.log("valid");
    	localStorage.setItem("token", token_id);
	localStorage.setItem("user", username);
    	window.location = url + "home/" + username +"/" + token_id;
    }else{
    	location.reload();
    }
    
});


$("#logout").click(function() {
    window.location.href = url + "beyond_login";
    console.log("logging out")
    var token = {};
    token["token_id"] = localStorage.getItem("token");;
    var json_token= JSON.stringify(token);
    console.log(json_token)
    $.ajax({
    	type : "DELETE",
    	url : url + "logout",
    	data: json_token,
    	contentType: 'application/json;charset=UTF-8',
    	headers: {
    	    'X-token':'',
    	    'Content-Type':'application/json'
    	},
    	success: function(result) {
    	    console.log(result);
    	},
    	async: false
    });
    localStorage.removeItem("token");
    localStorage.removeItem("user");

});


$("#home").click(function() {
    var token = localStorage.getItem("token");
    var username = localStorage.getItem("user");
    console.log(token)
    var url_ = url + "home/" + username +"/" + token;
    console.log(url_)
    window.location = url_ 
});


$("#manage").click(function() {
    var token = localStorage.getItem("token");
    var username = localStorage.getItem("user");
    console.log(token)
    var url_ = url + "home/" + username +"/" + token +"/battle";
    console.log(url_)
    window.location = url_ 
});



$("#create").click(function() {
    var token = localStorage.getItem("token");
    var username = localStorage.getItem("user");

    //console.log('test');
    var name = $('#battle_name').val();
    var start = $('#start').val();
    var end = $('#end').val();

    var battle = {};
    battle["name"] = name;
    battle["start"] = start;
    battle["end"] =end;
    var json_battle= JSON.stringify(battle);
    var url_ =url+'home/'+username+"/"+token+"/battle";
    console.log(url_);
    console.log(json_battle);
        $.ajax({
    	type : "POST",
    	    url : url_,
    	data: json_battle,
    	contentType: 'application/json;charset=UTF-8',
    	headers: {
    	    'X-token':'',
    	    'Content-Type':'application/json'
    	},
    	success: function(result) {
    	    console.log(result);
    	    result = JSON.parse(result);
    	    success = result['success'];
	    message = result['message'];
	    //console.log(message)
    	},
    	async: false
    });
    if (success==true){
	alert(message);
	console.log(message);
	window.location = url_; 
    }else{
	alert(message);
	console.log(message);
    	location.reload();
    }
});



$(".start").click(function() {
    var token = localStorage.getItem("token");
    var username = localStorage.getItem("user");

    var name = $(this).attr("id");
    console.log(name);

    var start_battle = {};
    start_battle["name"] = name;
    var json_start= JSON.stringify(start_battle);
    var url_ =url+"home/"+username+"/"+token+"/battle"+"/manage";
    console.log(url_);
    console.log(json_start);
        $.ajax({
    	type : "POST",
    	    url : url_,
    	data: json_start,
    	contentType: 'application/json;charset=UTF-8',
    	headers: {
    	    'X-token':'',
    	    'Content-Type':'application/json'
    	},
    	success: function(result) {
    	    console.log(result);
    	    result = JSON.parse(result);
    	    success = result['success'];
	    message = result['message'];
	    //console.log(message)
    	},
    	async: false
	});
    alert(message);
    location.reload();


    
});



$(".modify").click(function() {
    var _id = $(this).attr("id");
    var name = "#"+_id
    $(name).show();
    console.log("test");
});


$(".close_").click(function() {
    var _id = $(this).attr("id");
    var name = "#"+_id
    $(name).hide();
});

$(".save").click(function() {
    var token = localStorage.getItem("token");
    var username = localStorage.getItem("user");
    var _id = $(this).attr("id");
    var start = $('#start').val();
    var end = $('#end').val();

    var update = {};
    update["name"] = _id;
    update["start"] = start;
    update["end"] =end;
    var json_update= JSON.stringify(update);
    console.log(json_update);
    var url_ =url+"home/"+username+"/"+token+"/battle"+"/manage";
    console.log(url_);

    $.ajax({
    	type : "PUT",
    	url : url_,
    	data: json_update,
    	contentType: 'application/json;charset=UTF-8',
    	headers: {
    	    'X-token':'',
    	    'Content-Type':'application/json'
    	},
    	success: function(result) {
    	    console.log(result);
    	    result = JSON.parse(result);
    	    success = result['success'];
	    message = result['message'];
	    //console.log(message)
    	},
    	async: false
	});
    alert(message);
    location.reload();
});



$(".delete").click(function() {
    var token = localStorage.getItem("token");
    var username = localStorage.getItem("user");
    var _id = $(this).attr("id");
    var name = "#"+_id
    console.log(_id);
    var del_ = {};
    del_["name"] = _id;
    var json_del_= JSON.stringify(del_);
    console.log(json_del_);
    var url_ =url+"home/"+username+"/"+token+"/battle"+"/manage";
    console.log(url_);

    $.ajax({
    	type : "DELETE",
    	url : url_,
    	data: json_del_,
    	contentType: 'application/json;charset=UTF-8',
    	headers: {
    	    'X-token':'',
    	    'Content-Type':'application/json'
    	},
    	success: function(result) {
    	    console.log(result);
    	    result = JSON.parse(result);
    	    success = result['success'];
    	    message = result['message'];
    	    //console.log(message)
    	},
    	async: false
    	});
    alert(message);
    location.reload();

});
