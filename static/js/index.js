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

function addConnectedFunction(mac, functionName) {
	$.ajax({
		url: '/devices/' + mac + "/connected/" + functionName,
		method: 'POST',
		success: reloadFunction
	})		
}

function addDisconnectedFunction(mac, functionName) {
	$.ajax({
		url: '/devices/' + mac + "/disconnected/" + functionName,
		method: 'POST',
		success: reloadFunction
	})		
}

function removeConnectedFunction(mac, functionName) {
	$.ajax({
		url: '/devices/' + mac + "/connected/" + functionName,
		method: 'DELETE',
		success: reloadFunction
	})		
}

function removeDisconnectedFunction(mac, functionName) {
	$.ajax({
		url: '/devices/' + mac + "/disconnected/" + functionName,
		method: 'DELETE',
		success: reloadFunction
	})		
}


