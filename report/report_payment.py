# -*- coding: utf-8 -*-
from odoo import api, models
from odoo.addons.l10n_gt_extra import a_letras

class ReportAbstractPayment(models.AbstractModel):
    _name = 'texpasa.abstract.report_account_payment'

    def totales(self, o):
        t = {'debito': 0, 'credito': 0}
        for l in o.move_id.line_ids:
            t['debito'] += l.debit
            t['credito'] += l.credit
        return t

    def a_letras(self,monto):
        return a_letras.num_a_letras(monto)

    def fecha_larga(self, date):
        return str(date.day) + ' de ' + a_letras.mes_a_letras(date.month - 1) + ' de ' +  str(date.year)

    def _get_report_values(self, docids, data=None):
        model = 'account.payment'
        docs = self.env['account.payment'].browse(docids)

        return {
            'doc_ids': docids,
            'doc_model': model,
            'docs': docs,
            'data': data,
            'fecha_larga': self.fecha_larga,
            'a_letras': self.a_letras,
            'totales': self.totales,
        }

class ReportPayment1(models.AbstractModel):
    _name = 'report.texpasa.report_account_payment1'
    _inherit = 'texpasa.abstract.report_account_payment'