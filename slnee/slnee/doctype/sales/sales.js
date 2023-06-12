// Copyright (c) 2023, Weslati Baha Eddine and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales', {
	// refresh: function(frm) {

	// }
	simple:function(frm){
		if (frm.doc.simple){
			frm.doc.variable=0;
			refresh_field("variable")
		}else{
			frm.doc.variable=1;refresh_field("variable")
		}
		update_fct(frm)},
	variable:function(frm){
		if (frm.doc.variable){
			frm.doc.simple=0;
			refresh_field("simple");
		}else{
			frm.doc.simple=1;
			refresh_field("simple");
		}
		update_fct(frm);
	},
	categories:function(frm){update_fct(frm)},
	apply:function(frm){apply_button(frm)},
	percentage:function(frm){set_per(frm)},
	round:function(frm){set_per(frm)},
});


function set_per(frm){
	if (frm.doc.percentage && frm.doc.percentage>0){
	var per=(100-frm.doc.percentage)/100;
	for (var i =0;i<frm.doc.items.length;i++){
		frm.doc.items[i].sales_price=frm.doc.items[i].price*per
		if (frm.doc.round){
			frm.doc.items[i].sales_price=Math.round(frm.doc.items[i].sales_price)
		}
	}
	refresh_field("items")
	}
	else{
		for (var i =0;i<frm.doc.items.length;i++){
			frm.doc.items[i].sales_price=0;
		}
	refresh_field("items")

	}

}


function apply_button(frm){
	frappe.call({
		method:"apply_sales",
		doc:frm.doc

	})

}


function update_fct(frm){
	console.log("b");
	frappe.call({
		method:"update_items",
		doc:frm.doc,
		callback(r){
			refresh_field("items")
		}

	})


}
