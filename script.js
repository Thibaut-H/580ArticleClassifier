$(document).ready(function(){
	$('#trainingDataForms').append(
		'<form action="./cgi-bin/augmentData.py" method="post">');
	$('#trainingDataForms form').append(
		'<input type="text" name="tagName" placeholder="Classification"><br><br>');
	for(var i=0;i<10;++i){
		$('#trainingDataForms form').append(
			'<input type="text" name="urlForm' + i + '" placeholder="Article URL"><br>');
	}
	$('#trainingDataForms form').append(
		'<br><input type="submit" value="Submit"></form>');
});