# Copyright (c) 2022, Weslati Baha Eddine and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from slnee.slnee.doctype.wordpress_store.wordpress_store import get_api
from frappe import _
class AddItemstoStoreTool(Document):
	@frappe.whitelist()
	def insert_items(self):
		if self.category_type=="Create new category":
			category_name=self.new_category
			if not category_name:
				return
			doc=frappe.new_doc("Store Category")
			doc.name1=category_name
			doc.update_store=1
			item_group=frappe.get_doc("Item Group",self.item_group)
			if item_group.image:
				doc.image=item_group.image
			if not frappe.db.exists("Store Category",category_name):
				doc.insert(ignore_if_duplicate=True)
				frappe.db.commit()
		else:
			category_name=self.old_category
			if not category_name:
				return
		create=[]
		exist=0
		for i in self.items:
			if len(create)>9:
				break
			item=frappe.get_doc("Item",i.item)
			if frappe.db.exists("Store Item",i.item):
				if frappe.db.get_value("Store Item",i.item,"id"):
					exist+=1
					continue
				else:
					doc=frappe.get_doc("Store Item",i.item)
					create.append(doc.get_data())
					continue
			doc = frappe.new_doc('Store Item')
			doc.update_store=0
			doc.name1=i.item
			doc.warehouse=self.warehouse
			doc.type="simple"
			doc.status=self.status
			doc.items=[i]
			doc.manage_stock=1
			doc.stock_quantity=i.stock
			doc.sale_price=i.sale_price
			doc.on_sale=1 if doc.sale_price >0 else 0
			tax=i.price*0.15
			doc.tax=tax
			doc.desxription=item.description if item.description else ""

			doc.regular_price=i.price+tax
			doc.image_1 = item.image if item.image else ""
			category=doc.append("categories",{})
			category.category=category_name
			doc.insert()
			create.append(doc.get_data())
		#frappe.db.commit()
		#frappe.throw(str(create))
		data={"create":create}
		if True:
			wcapi=get_api(100)
			r=wcapi.post("products/batch", data).json()
			r=r["create"]
			for i in r:
				frappe.db.set_value("Store Item",i["name"],"id",i["id"])
				frappe.db.set_value("Store Item",i["name"],"permalink",i["permalink"])
			frappe.db.commit()
			frappe.msgprint(_("{} items were added to the shop succesfully.").format(len(create)),alert=True,indicator="green")
			self.items=[]
			self.get_items(self.item_group)
		else:
			frappe.throw("Unknown Error")
	@frappe.whitelist()
	def set_defaults(self):
		settings=frappe.get_doc("Wordpress Store")
		if not self.warehouse:
			self.warehouse=settings.default_warehouse or ""
		self.price_list=settings.price_list or ""
		self.tax_template=settings.sales_taxes_and_charges_template or ""


	@frappe.whitelist()
	def get_items(self,item_group):
		items=frappe.db.get_list("Item",filters={"item_group":item_group})
		self.items=[]
		have_price=self.have_price_list
		in_stock=self.in_stock
		n=0
		warehouses=[w.warehouse for w in self.warehouse]
		#frappe.throw(str(warehouses))
		for i in items:
			price=0
			stock=0
			rates=frappe.db.get_list("Item Price",filters={"item_code":i.name,"price_list":self.price_list},fields=["price_list_rate"],order_by="valid_from desc")
			if len(rates)>0:
				price=rates[0]["price_list_rate"]
			f=[["item_code",'in',[i.name]]]
			if len(warehouses)>0:
				f.append(["warehouse","in",warehouses])
			bins=frappe.db.get_list("Bin",filters=f,fields=["actual_qty"])
			for b in bins:
					stock+=b["actual_qty"]
			if (price or not have_price)  and (stock or not in_stock):
				if frappe.db.exists("Store Item",i["name"]):
					continue
				add=self.append("items",{})
				add.price=price
				add.stock=stock
				add.item=i["name"]
				n+=1
		self.items_number=n
