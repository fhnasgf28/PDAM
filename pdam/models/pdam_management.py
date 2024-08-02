from odoo import models, fields, api, _


class PdamManagement(models.Model):
    _name = 'pdam.management'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'PDAM Management'

    name = fields.Char(string='Customer Reference', copy=False, readonly=True, index=True)
    is_pdam = fields.Boolean(string="RFQ Created", default=True)
    description = fields.Text(string='Description')
    customer_number = fields.Char(string='Customer Number')
    date_field = fields.Date(string='Bulan Pembayaran')
    billing_period = fields.Char(string='Periode Tagihan', required=True, compute='_compute_month_name')
    start_date = fields.Date(string='Start Date', default=fields.Date.today)
    end_date = fields.Date(string='End Date')
    responsible_id = fields.Many2one('res.users', string='Responsible', required=True)
    # customer_ids = fields.One2many('res.partner', 'pdam_management_id', string='Customers')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('ongoing', 'Ongoing'),
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

    def action_start(self):
        self.state = 'ongoing'

    def action_complete(self):
        self.state = 'completed'

    def action_cancel(self):
        self.state = 'cancelled'
