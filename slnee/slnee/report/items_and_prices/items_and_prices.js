// Copyright (c) 2023, Weslati Baha Eddine and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Items and prices"] = {
	"filters": [
		{fieldname:'item_group',label: __('Item Group'),fieldtype: 'Link',options: 'Item Group'},
		
	]
};
