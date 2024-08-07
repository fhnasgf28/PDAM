from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = 'PDAM Partner'

    no_card_ID = fields.Char(string='No KTP', help='Nomor KTP pelanggan')
    meter_number = fields.Char(string='Meter Number', compute='_compute_meter_number')
    meter_install_date = fields.Date(string='Tanggal Pemasangan', help='Tanggal pemasangan meteran')
    last_reading = fields.Float(string='Current Reading')
    water_usage = fields.Float(string='Water Usage')
    pdam_management_id = fields.Many2one('pdam.management', string="Informasi Pelanggan")
    location_id = fields.Many2one('stock.location', string='Lokasi', help='Lokasi pemasangan meteran')
    status = fields.Selection([
        ('active', 'Aktif'),
        ('inactive', 'Tidak Aktif'),
        ('maintenance', 'Pemeliharaan'),
    ], string='Status', default='active', help='Status operasional meteran')

    @api.depends('no_card_ID')
    def _compute_meter_number(self):
        for record in self:
            if not record.no_card_ID:
                record.meter_number = ''
            else:
                record.meter_number = '45170' + '' + record.no_card_ID
