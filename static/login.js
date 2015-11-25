var token_id = 0;
var url = "http://herbportal.ddns.net/"

$("#login").click(function() {
    var username = $('#username').val();
    var password = $('#password').val();
    var user = {}
    user["username"] = username
    user["password"] = password
    var json_user= JSON.stringify(user);
    console.log(json_user);

    $.ajax({
	type : "POST",
	url : url + "beyond_login",
	data: user,
	contentType: 'application/json;charset=UTF-8',
	headers: {
	    'X-token':'',
	    'Content-Type':'application/json'
	},
	success: function(result) {
	    console.log(result);
	    // json_result = JSON.parse(result);
	    // token_id = json_result['data'];
	    // console.log(json_result);
	},
	async: false
    });

    // if(token_id){
    // 	console.log("valid");
    // 	console.log(token_id);
    // 	localStorage.setItem("token", token_id);
    // 	window.location.href = url + "home";
    // }else{
    // 	console.log(user);
    // 	location.reload();
    // }

}); 
