import frappe


def recalculate_completed_qty_in_intern_sales_order(doc,method):
    if doc.intern_sales_order!=None:
        change_doc_status_falg=False
        intern_sales_order=frappe.get_doc("Intern Sales Order",doc.intern_sales_order)
        for item in intern_sales_order.items:  
            if item.item_code==doc.production_item:
                item.ordered_qty=item.ordered_qty-doc.qty
            else:
                if item.ordered_qty>0:
                    change_doc_status_falg=1
        
        if not change_doc_status_falg:
            intern_sales_order.status="Open"
        
        intern_sales_order.save()