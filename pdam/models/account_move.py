from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'account.move'
    _description = 'Account Move PDAM'

    is_paid = fields.Boolean(string="Is Paid", default=False)
