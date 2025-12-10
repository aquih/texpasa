# -*- encoding: utf-8 -*-

from odoo import models, fields, Command, api, _
from odoo.exceptions import UserError, ValidationError
import logging

class AccountMove(models.Model):
    _inherit = "account.move"

    def generar_diferencial(self):
        for factura in self:
            if factura.currency_id == factura.company_id.currency_id:

                if not factura.journal_id.compania_relacionada_id:
                    raise ValidationError('No existe compañía fiscal relacionada en el diario.')

                for pago in factura.matched_payment_ids:
                    if len(self.env['account.move'].with_company(factura.journal_id.compania_relacionada_id).search([('journal_id','=',factura.journal_id.compania_relacionada_id.currency_exchange_journal_id.id), ('ref','=',pago.name)])) == 0:

                        valor_fecha_factura = factura.currency_id._convert(pago.amount, factura.journal_id.compania_relacionada_id.currency_id, company=factura.journal_id.compania_relacionada_id, date=factura.invoice_date, round=False)
                        valor_fecha_pago = factura.currency_id._convert(pago.amount, factura.journal_id.compania_relacionada_id.currency_id, company=factura.journal_id.compania_relacionada_id, date=pago.date, round=False)

                        diferencial = valor_fecha_pago - valor_fecha_factura

                        asiento = self.env['account.move'].with_company(factura.journal_id.compania_relacionada_id).create({
                            'move_type': 'entry',
                            'ref': pago.name,
                            'journal_id': factura.journal_id.compania_relacionada_id.currency_exchange_journal_id.id,
                            'company_id': factura.journal_id.compania_relacionada_id.id,
                            'date': pago.date
                        })
                        asiento.line_ids = [Command.create({
                            'name': 'Diferencial ambiaro entre compañías Texpasa',
                            'account_id': factura.with_company(factura.journal_id.compania_relacionada_id).partner_id.property_account_receivable_id.id,
                            'debit': abs(diferencial) if diferencial > 0 else 0,
                            'credit': abs(diferencial) if diferencial < 0 else 0,
                        }), Command.create({
                            'name': 'Diferencial ambiaro entre compañías Texpasa',
                            'account_id': factura.journal_id.compania_relacionada_id.income_currency_exchange_account_id.id,
                            'debit': abs(diferencial) if diferencial < 0 else 0,
                            'credit': abs(diferencial) if diferencial > 0 else 0,
                        })]

                        asiento._post()
