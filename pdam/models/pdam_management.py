from odoo import models, fields, api


class PdamManagement(models.Model):
    _name = 'pdam.management'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'PDAM Management'

    name = fields.Char(string='Customer Reference', required=True, copy=False, readonly=True, index=True)
    description = fields.Text(string='Description')
    customer_number = fields.Char(string='Customer Number', required=True)
    billing_period = fields.Selection([
        ('januari', 'Januari'),
        ('februari', 'Februari'),
        ('maret', 'Maret'),
        ('april', 'April'),
        ('mei', 'Mei'),
        ('juni', 'Juni'),
        ('juli', 'Juli'),
        ('agustus', 'Agustus'),
        ('september', 'September'),
        ('oktober', 'Oktober'),
        ('november', 'November'),
        ('desember', 'Desember')
    ], string='Periode Tagihan', required=True, default='januari')
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

    def action_start(self):
        self.state = 'ongoing'

    def action_complete(self):
        self.state = 'completed'

    def action_cancel(self):
        self.state = 'cancelled'
