from odoo import models, fields, api, _


class PdamManagement(models.Model):
    _name = 'pdam.management'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'PDAM Management'

    name = fields.Char(string='Customer Reference', copy=False, readonly=True, index=True)
    product_id = fields.Many2one('product.template', string='PDAM', required=True)
    customer_id = fields.Many2one('res.partner', string='Customer', required=True)
    price_per_cubic = fields.Float('Harga per kubik', readonly=True, default=3000)
    is_pdam = fields.Boolean(string="RFQ Created", default=True)
    is_paid = fields.Boolean(string="Is Paid", default=False)
    description = fields.Text(string='Description')
    customer_number = fields.Char(string='Customer Number')
    date_field = fields.Date(string='Tanggal Pembayaran')
    billing_period = fields.Char(string='Periode Tagihan', required=True, compute='_compute_month_name', store=True)
    responsible_id = fields.Many2one('res.users', string='Responsible', required=True)
    customer_ids = fields.One2many('res.partner', 'pdam_management_id', string='Customers')
    total_payment = fields.Float(string='Total Pembayaran', compute='_compute_total_payment')
    cubic_quantity = fields.Float(string='Jumlah Kubik')
    cubics_last_month = fields.Float(string='Jumlah Kubik Bulan Lalu')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('bayar', 'Di Bayar'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft')

    @api.model
    def create(self, vals):
        if vals.get('is_pdam'):
            sequence_code = 'seq.pdam.management'
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(sequence_code) or _('New')
        res = super(PdamManagement, self).create(vals)
        return res

    @api.depends('date_field')
    def _compute_month_name(self):
        for record in self:
            if record.date_field:
                record.billing_period = record.date_field.strftime('%B')
            else:
                record.billing_period = ''

    @api.depends('cubic_quantity')
    def _compute_total_payment(self):
        for record in self:
            record.total_payment = self.cubic_quantity * 3000

    def action_complete(self):
        self.state = 'completed'

    def action_cancel(self):
        self.state = 'cancelled'

    def action_create_invoice(self):
        invoice_obj = self.env['account.move']
        invoice_vals = {
            'partner_id': self.customer_id.id,
            'move_type': 'out_invoice',
            'name': self.name,
            'is_paid': True,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product_id.id,
                'quantity': self.cubic_quantity,
                'price_unit': self.price_per_cubic
            })],
        }
        invoice = invoice_obj.create(invoice_vals)
        self.is_paid = True
        return {
            'name': 'Customer Invoice',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }


class PdamManagementLine(models.Model):
    _name = 'pdam.management.line'
    _description = 'Informasi Meteran PDAM'

    meter_id = fields.Char(string='Meter ID', required=True, help='ID atau nomor identifikasi meteran')
    location = fields.Char(string='Lokasi', help='Lokasi pemasangan meteran')
    capacity = fields.Float(string='Kapasitas', help='Kapasitas maksimum meteran dalam liter')
    status = fields.Selection([
        ('active', 'Aktif'),
        ('inactive', 'Tidak Aktif'),
        ('maintenance', 'Pemeliharaan'),
    ], string='Status', default='active', help='Status operasional meteran')
    installation_date = fields.Date(string='Tanggal Pemasangan', help='Tanggal pemasangan meteran')
    last_maintenance_date = fields.Date(string='Tanggal Pemeliharaan Terakhir',
                                        help='Tanggal terakhir meteran dipelihara')
    partner_id = fields.Many2one('res.partner', string='Pelanggan', help='Pelanggan yang menggunakan meteran ini')
    res_partner_ids = fields.One2many('res.partner', 'pdam_management_id', string="Informasi Pelanggan")
