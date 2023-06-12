# Copyright (c) 2023, Weslati Baha Eddine and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from slnee.slnee.doctype.wordpress_store.wordpress_store import get_api
from frappe import _
class Sales(Document):
	

	@frappe.whitelist()
	def apply_sales(self):
		update=[]
		if self.simple:
			for i in self.items:
				if i.sales_price>0:
					update.append({"id":i.id,"sale_price":str(i.sales_price),"on_sale":True})
				else:
					update.append({"id":i.id,"sale_price":"","on_sale":False})

			wcapi=get_api(100)
			data={"update":update}
			r=wcapi.post("products/batch", data).json()
			#frappe.throw(str(r))
			for i in r["update"]:
				try:
					if not i["sale_price"]:
						sale_price=0
					else:
						sale_price=float(i["sale_price"])
					frappe.db.set_value("Store Item",i["name"],"sale_price",sale_price)
					on_sale=1 if i["on_sale"] else 0
					frappe.db.set_value("Store Item",i["name"],"on_sale",on_sale)
				except:
					continue
			alert("Sales Prices have been set successfully")
		else:
			n=0
			wcapi=get_api(100)
			parent_ids=[i.parent_id for i in self.items]
			parent_ids=list(set(parent_ids))
			for p in parent_ids:
				url="products/"+str(p)
				update=[]
				variables={}
				prices={}
				for i in self.items:
					if i.parent_id==p:
						variables[int(i.id)]=i.variable_name
						prices[int(i.id)]=i.sales_price
						if i.sales_price>0:
							update.append({"id":i.id,"sale_price":str(i.sales_price*1.15),"on_sale":True})
						else:
							update.append({"id":i.id,"sale_price":"","on_sale":False})
				if len(update)==0:
					continue
				#frappe.throw(str(variables))
				data={"update":update}
				r=wcapi.post(url+"/variations/batch",data).json()
				n+=1
				for i in r["update"]:
					if True:
						name=variables[int(i["id"])]
						price=prices[int(i["id"])]
						frappe.db.set_value("Store Item List",name,"sale_price",price)
					else:
						pass
			alert("{} Variable Item(s) has been updated".format(n))
	@frappe.whitelist()
	def update_items(self):
		cat=[i.category for i in self.categories]
		filters=[]
		cond=""
		if len(cat)>0:
			cat=str(tuple(cat))
			cat=cat.replace(",)",")")
			cond=" and it.category in "+cat
		simple=False
		if self.simple and not self.variable:
			cond+=" and i.type= 'simple'"
			sql="select distinct i.name,i.regular_price,i.sale_price,i.id from `tabStore Item` as i, `tabStore Category Item` as it where it.parent=i.name "
			simple=True
		if self.variable and not self.simple:
			cond+=" and i.type= 'variable'"
			sql="select distinct itl.item,itl.price,itl.sale_price,itl.id,itl.parent,i.id,itl.name from `tabStore Item` as i, `tabStore Category Item` as it, `tabStore Item List` as itl where it.parent=i.name and i.name=itl.parent"
		sql+=cond
		res=frappe.db.sql(sql)
		res=list(res)
		self.items=[]
		for r in res:
			item=self.append("items",{})
			if simple:
				item.item=r[0]
			else:
				item.parent_id=r[5]
				item.variable_name=r[6]
				item.item="{} (<a style='color:blue;' href='/app/store-item/{}' >{}</a>)".format(r[0],r[4],r[4])
			item.sales_price=r[2]
			item.price=r[1]
			item.id=r[3]

def alert(msg,color="green"): 
	frappe.msgprint( _(msg), alert=True, indicator=color)
