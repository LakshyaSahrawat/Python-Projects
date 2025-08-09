import frappe
from frappe.utils import nowdate

def get_context(context):
    # Handle delete request
    if frappe.form_dict.get("delete_name"):
        try:
            frappe.delete_doc("Electricity Bill", frappe.form_dict.delete_name, ignore_permissions=True)
            frappe.db.commit()
            context.message = "Bill deleted successfully!"
        except Exception as e:
            context.error = f"Error deleting bill: {str(e)}"

    # Handle new bill creation
    elif frappe.form_dict.get("consumer_name") and frappe.form_dict.get("units_consumed"):
        consumer_name = frappe.form_dict.consumer_name.strip()

        try:
            units = float(frappe.form_dict.units_consumed)
        except ValueError:
            context.error = "Invalid input for Units Consumed."
            units = None

        if units is not None:
            if units < 0 or units > 1000:
                context.error = "Units Consumed must be between 0 and 1000."
            else:
                try:
                    bill = frappe.get_doc({
                        "doctype": "Electricity Bill",
                        "consumer_name": consumer_name,
                        "units_consumed": units,
                        "billing_date": nowdate()
                    })
                    bill.insert(ignore_permissions=True)
                    frappe.db.commit()
                    context.message = "Bill created successfully!"
                except Exception as e:
                    context.error = f"Error: {str(e)}"

    # Fetch past bills
    context.bills = frappe.get_all(
        "Electricity Bill",
        fields=["name", "billing_date", "consumer_name", "units_consumed", "rate_per_unit", "total_amount"],
        order_by="billing_date desc"
    )

    # Fetch monthly summary
    monthly_data = frappe.db.sql("""
        SELECT DATE_FORMAT(billing_date, '%M %Y') AS month,
               SUM(units_consumed) AS total_units
        FROM `tabElectricity Bill`
        GROUP BY DATE_FORMAT(billing_date, '%Y-%m')
        ORDER BY MIN(billing_date) DESC
    """, as_dict=True)

    context.monthly_summary = monthly_data

    return context

