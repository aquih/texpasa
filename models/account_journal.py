# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging

class AccountJournal(models.Model):
    _inherit = "account.journal"

    compania_relacionada_id = fields.Many2one('res.company', string='Compañía Fiscal Relacionada', index=True, ondelete='restrict')