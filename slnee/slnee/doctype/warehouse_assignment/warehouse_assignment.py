# Copyright (c) 2023, Weslati Baha Eddine and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class WarehouseAssignment(Document):
	

	@frappe.whitelist()
	def select_all(self):
		warehouses=frappe.db.get_list("Warehouse",filters={"is_group":0,"disabled":0})
		self.warehouses=[]
		for w in warehouses:
			ww=self.append("warehouses",{})
			ww.warehouse=w["name"]
