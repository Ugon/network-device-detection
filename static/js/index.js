function removeMac(mac) {
	$.ajax({
		url: '/devices/' + mac,
		method: 'DELETE',
		success: function() {
			location.reload(true)
		}
	})
}

function addMacFromInput() {
	newMac = $('#new-mac-input').val()
	$.ajax({
		url: '/devices/' + newMac,
		method: 'POST',
		success: function() {
			location.reload(true)
		}
	})
}