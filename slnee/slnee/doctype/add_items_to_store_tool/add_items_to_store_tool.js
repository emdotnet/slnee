// Copyright (c) 2022, Weslati Baha Eddine and contributors
// For license information, please see license.txt

frappe.ui.form.on('Add Items to Store Tool', {
	refresh: function(frm) {
		frm.call({
			doc:frm.doc,
			method: 'set_defaults'})
	//$(".btn-primary").hide();
	//$(".indicator-pill").hide();
	},
	item_group: function(frm){refresh_items(frm)},
	have_price_list: function(frm){refresh_items(frm)},
	in_stock: function(frm){refresh_items(frm)},
	insert:function(frm){insert_items(frm)},
	warehouse:function(frm){
		refresh_items(frm)
	},
});

frappe.ui.form.on("Store Item List",{

	item(frm,cdt,cdn){
		var warehouses=[];
		if (frm.doc.warehouse){
			for (var i=0;i<frm.doc.warehouse.length;i++){
			warehouses.push(frm.doc.warehouse[i].warehouse)
		}}
		let item= frappe.get_doc(cdt, cdn);
		frappe.call({
			async:false,
			args:{"item":item.item,"warehouse":warehouses},
			method:"slnee.slnee.doctype.store_item.store_item.get_item_info",
			callback(r) {
				if(r.message){
					var ans=r.message.split("#");
					item.price=parseFloat(ans[0]);
					item.tax=parseFloat(ans[2])
					item.stock=parseFloat(ans[1]);
				}
			}
		})
		frm.refresh_field("items");
		}


})



function insert_items(frm){
	frm.call({
		doc:frm.doc,
		method: 'insert_items',
		freeze:true,
		freeze_message: __("Inserting Items"),
	})
};
function refresh_items(frm){
	frm.call({
		doc:frm.doc,
		args:{"item_group":frm.doc.item_group},
		freeze: true,
		freeze_message: __("Fetching Items"),
		method: 'get_items',
		})
}
