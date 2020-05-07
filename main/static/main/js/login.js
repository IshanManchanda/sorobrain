$(document).ready(function () {

	$('ul.tabs').tabs(swipeable: true);

	$('#btnContinue').click(function () {
		$('ul.tabs').tabs('select_tab', 'register');
	});
});