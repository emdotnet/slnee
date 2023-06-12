// Copyright (c) 2023, Weslati Baha Eddine and contributors
// For license information, please see license.txt

frappe.ui.form.on('Warehouse Assignment', {
	// refresh: function(frm) {

	// }
	user:function(frm){
		frappe.call({
			doc:frm.doc,
			method:"select_all",
		callback: function(r){
			refresh_field("warehouses")
		}
		});
	},
	select_all:function(frm){
		for (var i =0;i<frm.doc.warehouses.length;i++){
			frm.doc.warehouses[i].enabled=1;
			frm.doc.warehouses[i].delivery_note=1;
		}
		frm.set_value("select_all",1);
		refresh_field("warehouses")
	},
	unselect_all:function(frm){
		for (var i =0;i<frm.doc.warehouses.length;i++){
			frm.doc.warehouses[i].enabled=0;
			frm.doc.warehouses[i].delivery_note=0;
		}
		frm.set_value("unselect_all",1);
		refresh_field("warehouses")

	}
});
