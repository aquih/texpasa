# -*- encoding: utf-8 -*-

from odoo import models, fields, Command, api, _
from odoo.exceptions import UserError, ValidationError
import logging

class AccountPayment(models.Model):
    _inherit = "account.payment"

    def _compute_reconciliation_status(self):
        super(AccountPayment, self)._compute_reconciliation_status()
        for pago in self:
            for factura in pago.reconciled_invoice_ids:
                factura.generar_diferencial()
