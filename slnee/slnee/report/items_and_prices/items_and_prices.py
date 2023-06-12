# Copyright (c) 2023, Weslati Baha Eddine and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns=get_columns(filters=filters)
	if "item_group" in filters.keys() and filters["item_group"]:
		sql="select distinct ip.item_code,ip.price_list_rate,i.image,i.item_group from `tabItem Price` as ip, `tabItem` as i  where i.name=ip.item_code and ip.selling=1 and i.item_group=%(group)s"
		sql_data=frappe.db.sql(sql,values={"group":filters["item_group"]})
	else:
		sql="select distinct ip.item_code,ip.price_list_rate,i.image,i.item_group from `tabItem Price` as ip, `tabItem` as i  where i.name=ip.item_code  and ip.selling=1;"
		sql_data=frappe.db.sql(sql)
	for r in sql_data:
		try:
			data.append({"item":r[0],"rate":r[1],"image":"<span><img style='max-height:110px;width:auto !important;' src='"+r[2]+"'></span>","item_group":r[3]})
		except:
			try:
				data.append({"item":r[0],"rate":r[1],"image":"","item_group":r[3]})
			except:
				continue
	return columns, data





def get_columns(filters=None):
	columns=[]
	columns.append(('Item') + ":Link/Item:260")
	columns.append(('Item Group') + ":Link/Item Group:220")
	columns.append( ('Rate') + ":Data:160")
	columns.append( ('Image') + ":Data:200")

	return(columns)
