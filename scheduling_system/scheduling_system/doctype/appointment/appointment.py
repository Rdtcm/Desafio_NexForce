# flake8: noqa
# Copyright (c) 2025, Ryan Ledo and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe
from frappe.utils import format_datetime
from frappe import _


class Appointment(Document):
    def validate(self):
        # frappe.msgprint("🚨 Entrou no validate()")

        # mensagens de log para fins de debugar
        frappe.msgprint(f"Start Date: {self.start_date}")  # type: ignore
        frappe.msgprint(f"End Date: {self.end_date}")  # type: ignore
        frappe.msgprint(f"Seller: {self.seller}")  # type: ignore

        self.validate_seller_conflict()

    def validate_seller_conflict(self):
        # metodo para realizar a validacao

        overlapping_appointments = frappe.db.get_all(
            "Appointment",
            fields=["name", "start_date", "end_date"],
            filters=[
                ["seller", "=", self.seller],  # type: ignore
                ["name", "!=", self.name if self.name else ""],
                ["start_date", "<", self.end_date],  # type: ignore
                ["end_date", ">", self.start_date],  # type: ignore
            ]
        )

        # frappe.msgprint("Entrou na validacao!!!")

        for appt in overlapping_appointments:
            frappe.throw(_(
                "Seller {0} is already booked from {1} to {2}."
            ).format(
                self.seller,  # type: ignore
                format_datetime(appt["start_date"]),
                format_datetime(appt["end_date"])
            ))
