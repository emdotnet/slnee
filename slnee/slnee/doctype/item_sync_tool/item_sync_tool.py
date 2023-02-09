# Copyright (c) 2022, Weslati Baha Eddine and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from slnee.slnee.doctype.wordpress_store.wordpress_store import get_api
from frappe import _

class ItemSyncTool(Document):



	@frappe.whitelist()
	def add_items(self,cat):
		if not cat:
			return
		old=[i.item for i in self.items ]
		store_category_items=frappe.db.get_list("Store Category Item",filters={"category":cat},fields=["parent"])
		for i in store_category_items:
			if i["parent"] not in old:
				item=self.append("items",{})
				item.item=i["parent"]
				item.new_name=i["parent"]
				item.description=frappe.db.get_value("Store Item",i["parent"],"description")
				item.short_description=frappe.db.get_value("Store Item",i["parent"],"short_description")
				item.id=frappe.db.get_value("Store Item",i["parent"],"id")
				old.append(i["parent"])
	@frappe.whitelist()
	def rename_items(self):
		update=[]
		news=[]
		frappe.db.savepoint(save_point="before_rename_tool")
		for i in self.items:
			if True:
				u={"id":i.id,"name":i.new_name,"description":i.description,"short_description":i.short_description}
				frappe.db.set_value("Store Item",i.item,"short_description",i.short_description)
				frappe.db.set_value("Store Item",i.item,"description",i.description)
				frappe.db.set_value("Store Item",i.item,"name1",i.new_name)
				frappe.db.set_value("Store Item",i.item,"name",i.new_name)
				store_category_items=frappe.db.get_list("Store Category Item",filters={"parent":i.item},fields=["name"])
				for s in store_category_items:
					frappe.db.set_value("Store Category Item",s["name"],"parent",i.new_name)
				update.append(u)
				n={"name":i.new_name,"description":i.description,"short_description":i.short_description}
				news.append(n)
		wcapi=get_api(15)
		data={"update":update}
		r=wcapi.post("products/batch", data).json()
		self.items=[]
		for n in news:
			item=self.append("items",{})
			item.item=n["name"]
			item.new_name=n["name"]
			item.description=n["description"]
			item.short_description=n["short_description"]
		return r
		#frappe.rename_doc("Store Item",i.item,i.new_name)
		#frappe.db.rollback(save_point="before_rename_tool")
