from odoo import models, fields, api
from odoo.exceptions import UserError


class purchase_requests(models.Model):
    _name = 'purchase.requests'
    _description = 'purchase_requests'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'request_name'

    # Basic Information Fields
    request_name = fields.Char(string='Request Name', required=True)
    request_by = fields.Many2one(
        'res.users', string='Requested By', required=True,
        default=lambda self: self.env.user)
    start_date = fields.Date(string='Start Date', default=fields.Date.context_today)
    end_date = fields.Date(string='End Date')
    rejection_reason = fields.Text(string='Rejection Reason')

    # One2many line for order details
    order_line = fields.One2many(
        'purchase.requests.line', 'request_id', string='Order Lines')

    # Computed Total Price
    total_price = fields.Float(string='Total Price', compute='_compute_total_price', store=True)

    # Workflow state field
    state = fields.Selection(
        [('draft', 'Draft'),
         ('to be approved', 'To Be Approved'),
         ('approve', 'Approve'),
         ('reject', 'Reject'),
         ('cancel', 'Cancel')
         ],
        string='Status',
        default='draft',
        readonly=True,
        tracking=True
    )

    # Constraint: End date should not be before start date
    @api.constrains('end_date')
    def _check_end_date(self):
        for request in self:
            if request.end_date and request.end_date < request.start_date:
                raise UserError("End date cannot be earlier than start date.")

    # Compute total price from line totals
    @api.depends('order_line.total')
    def _compute_total_price(self):
        for request in self:
            request.total_price = sum(line.total for line in request.order_line)

    # Move to "To Be Approved" state
    def action_submit(self):
        self.state = 'to be approved'

    # Approve the request and send email to purchase managers
    def action_approve(self):
        self.ensure_one()
        self.state = 'approve'
        purchase_manger_group = self.env.ref('purchase.group_purchase_manager')
        users = purchase_manger_group.users
        subject = f"Purchase Request ({self.request_name}) Approved"
        body = f"<p>The purchase request <strong>{self.request_name}</strong> has been approved.</p>"
        for user in users:
            if user.partner_id.email:
                self.env['mail.mail'].create({
                    'subject': subject,
                    'body_html': body,
                    'email_to': user.partner_id.email,
                }).send()

    # Reset to draft state
    def action_reset(self):
        self.state = 'draft'

    # Cancel the request
    def action_cancel(self):
        self.state = 'cancel'

    # Trigger rejection wizard
    def action_reject(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Reject Request',
            'res_model': 'purchase.requests.reject.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_request_id': self.id,
            }
        }
