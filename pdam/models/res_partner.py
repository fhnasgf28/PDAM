from odoo import models, fields, api, _
from datetime import timedelta


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
    last_payment_date = fields.Date(string='Last Payment Date', compute="_compute_last_payment_date", store=True)

    @api.depends('no_card_ID')
    def _compute_meter_number(self):
        for record in self:
            if not record.no_card_ID:
                record.meter_number = ''
            else:
                record.meter_number = '45170' + '' + record.no_card_ID

    def _compute_last_payment_date(self):
        for partner in self:
            # mendapatkan faktur yang sudah dibayar dari customer
            last_paid_invoice = self.env['account.move'].search([
                ('partner_id', '=', partner.id),
                ('state', '=', 'posted'),
                ('payment_state', '=', 'paid')
            ], order='invoice_date desc', limit=1)
            #mengupdate last_payment_date dengan tanggal pembayaran terakhir
            partner.last_payment_date = last_paid_invoice.invoice_date if last_paid_invoice else False

    def _check_payment_status_and_send_whatsapp(self):
        #mendapatkan tanggal 2 bulan yang lalu
        two_month_ago = fields.Date.context_today(self) - timedelta(days=60)
        #memfilter customer yang belum membayar dalam 2 bulan terakhir
        customers_to_notify = self.search([
            ('last_payment_date', '<', two_month_ago),
            ('last_payment_date', '!=', False),
            ('mobile', '!=', False)
        ])

        for customer in customers_to_notify:
            whatsapp_url = f"https://wa.me/{customer.mobile.replace(' ', '').replace('+', '')}?text=Your%20payment%20is%20overdue.%20Please%20make%20a%20payment%20as%20soon%20as%20possible."
            # Kirim pesan WhatsApp
            customer.message_post(body=f"Pesan WhatsApp terkirim ke {customer.mobile}")
            # Tindakan lain jika diperlukan, seperti membuka URL
            self.env['ir.actions.act_url'].create({
                'type': 'ir.actions.act_url',
                'url': whatsapp_url,
                'target': 'new',
            })

    def action_open_whatsapp(self):
        self.ensure_one()
        if self.mobile:
            whatsapp_url = f"https://wa.me/{self.mobile.replace(' ', '').replace('+', '')}"
            return {
                'type': 'ir.actions.act_url',
                'url': whatsapp_url,
                'targe': 'new',
            }
        else:
            return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
            'title': _('Warning'),
            'message': 'Masukan Mobile Phone',
            'sticky': True,
            }
     }