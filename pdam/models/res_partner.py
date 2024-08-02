from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = 'PDAM Partner'

    meter_number = fields.Char(string='Meter Number')
    meter_install_date = fields.Date(string='Meter Install Date')
    last_reading = fields.Float(string='Current Reading')
    water_usage = fields.Float(string='Water Usage')