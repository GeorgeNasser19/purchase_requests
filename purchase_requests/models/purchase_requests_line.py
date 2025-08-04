from odoo import models, fields, api


class purchase_requests_line(models.Model):
    _name = 'purchase.requests.line'
    _description = 'purchase_requests_line'

    # Product reference
    product_id = fields.Many2one(
        'product.product', string='Product', required=True,)

    # Reference to the purchase request
    request_id = fields.Many2one('purchase.requests', string='Purchase Request')

    # Quantity of the product
    quantity = fields.Float(string='Quantity', required=True, default=1.0,)

    # Description of the product or line
    description = fields.Text(string='Description', required=True,)

    # Cost price per unit
    cost_price = fields.Float(string='Cost Price', required=True, default=0.0)

    # Total cost (quantity * cost price)
    total = fields.Float(string='Total', compute='_compute_total', store=True)

    # Compute the total value based on quantity and cost price
    @api.depends('quantity', 'cost_price')
    def _compute_total(self):
        for line in self:
            line.total = line.quantity * line.cost_price

    # Auto-fill cost and description based on selected product
    @api.onchange('product_id')
    def _onchange_product_id(self):
        for line in self:
            if line.product_id:
                line.cost_price = line.product_id.standard_price
                line.description = line.product_id.name
            else:
                line.cost_price = 0.0
                line.description = ''
