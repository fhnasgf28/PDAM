from odoo import models, fields
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'account.move'
    _description = 'Account Move PDAM'

    is_paid = fields.Boolean(string="Is Paid", default=False)

    def action_send_email(self):
        for record in self:
            if record.state != "posted":
                raise ValidationError("You can only send emails for posted invoices.")
            # email template
            template_id = self.env.ref("pdam.email_template_invoice_paid")
            template = self.env["mail.template"].browse(template_id)

            if template:
                template.send_mail(record.id, force_send=True)
            else:
                raise ValidationError("Email Template Not found")