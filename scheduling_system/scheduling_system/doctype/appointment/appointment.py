# flake8: noqa
# Copyright (c) 2025, Ryan Ledo and contributors
# For license information, please see license.txt


from frappe.model.document import Document
import frappe
from frappe.utils import format_datetime, add_to_date
from frappe import _
from datetime import datetime


class Appointment(Document):
    def validate(self):
        if not self.end_date:
            duration_in_minutes = self.duration_to_minutes(
                self.duration)  # type: ignore
            self.end_date = add_to_date(
                self.start_date, minutes=duration_in_minutes)  # type: ignore

        self.validate_seller_conflict()

    def duration_to_minutes(self, duration: str) -> int:
        # Metodo para converter a duracao de string para inteiro
        h, m, s = [int(x) for x in duration.split(':')]

        return h * 60 + m + int(s / 60)

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

        for appt in overlapping_appointments:
            frappe.throw(_(
                "Seller {0} is already booked from {1} to {2}."
            ).format(
                self.seller,  # type: ignore
                format_datetime(appt["start_date"]),
                format_datetime(appt["end_date"])
            ))
