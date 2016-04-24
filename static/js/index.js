function reloadFunction() {
	location.reload(true)
}

function removeMac(mac) {
	$.ajax({
		url: '/devices/' + mac,
		method: 'DELETE',
		success: reloadFunction
	})
}

function addMacFromInput() {
	newMac = $('#new-mac-input').val()
	$.ajax({
		url: '/devices/' + newMac,
		method: 'POST',
		success: reloadFunction
	})
}

function setAliasFromInput(mac) {
	var alias = $('#alias-input').val();
	$.ajax({
		url: '/devices/' + mac + "/alias/" + alias,
		method: 'POST',
		success: reloadFunction
	})
}

