# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class Company(models.Model):
    _inherit = "res.company"

    compania_relacionada_id = fields.Many2one('res.company', string='Compañía fiscal relacionada', index=True, ondelete='restrict')
