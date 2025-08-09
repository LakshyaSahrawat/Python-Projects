import frappe
from frappe.model.document import Document

class ElectricityBill(Document):
    def before_save(self):
        if not self.rate_per_unit:
            self.rate_per_unit = 7

        self.total_amount = float(self.units_consumed or 0) * float(self.rate_per_unit or 0)

        if self.units_consumed < 0 or self.units_consumed > 1000:
            frappe.throw("Units Consumed must be between 0 and 1000.")

