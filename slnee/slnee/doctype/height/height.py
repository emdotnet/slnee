# Copyright (c) 2022, Weslati Baha Eddine and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from slnee.slnee.doctype.wordpress_store.wordpress_store import get_api
from frappe import _

class height(Document):
	

	def after_rename(self,old,new,merge):
		l=frappe.db.get_list("Store Item List",filters={"term":new},fields=["*"])
		update=[]
		items=[]
		for i in l:
			if i["id"]:
				#attribute=frappe.db.get_value("Store Item",i["parent"],"attribute")
				#u={"id":i["id"],"attributes":[{"name":attribute,"option":i["term"]}]}
				items.append(i["parent"])
				#update.append(u)
		items=list(set(items))
		data={"update":update}
		wcapi=get_api()
		#frappe.throw(str(items))
		for i in items:
			doc=frappe.get_doc("Store Item",i)
			doc.sync_to_store(wcapi=wcapi)
			continue
			id=frappe.db.get_value("Store Item",i,"id")
			r=wcapi.post("products/"+id+"/variations/batch", data).json()
