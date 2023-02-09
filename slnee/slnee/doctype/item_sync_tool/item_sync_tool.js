// Copyright (c) 2022, Weslati Baha Eddine and contributors
// For license information, please see license.txt

frappe.ui.form.on('Item Sync Tool', {
	// refresh: function(frm) {

	// }
	add_items:function(frm){add_items(frm)},
	remove_all:function(frm){frm.items=[];refresh_field("items")},
	rename :function(frm){rename(frm)},
});




function rename(frm){
	frm.call({
		doc:frm.doc,
		method: "rename_items",
		freeze:true,
		freeze_message:__("Renaming items"),
		callback(r){
			console.log(r.message)
		}
	})
};

function add_items(frm){
	frm.call({
		doc:frm.doc,
		args:{"cat":frm.doc.category},
		method: 'add_items',
		freeze:true,
		freeze_message:__("Inserting Items"),
	})
}
