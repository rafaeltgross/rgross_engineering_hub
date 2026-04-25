from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProjectExpense(models.Model):
    _name = 'rgross.project.expense'
    _description = 'Project Expense'
    _order = 'date desc, id desc'

    name = fields.Char(string='Expense Name', required=True)
    project_id = fields.Many2one(
        'rgross.engineering.project',
        string='Project',
        required=True,
        ondelete='cascade',
    )
    date = fields.Date(string='Date', default=fields.Date.today)
    expense_type = fields.Selection([
        ('material', 'Material'),
        ('electronic_component', 'Electronic Component'),
        ('3d_printing', '3D Printing'),
        ('prototype', 'Prototype'),
        ('software_license', 'Software License'),
        ('supplier_service', 'Supplier Service'),
        ('travel', 'Travel'),
        ('shipping', 'Shipping'),
        ('other', 'Other'),
    ], string='Expense Type')
    vendor_id = fields.Many2one('res.partner', string='Vendor')
    amount = fields.Monetary(string='Amount', currency_field='currency_id')
    currency_id = fields.Many2one(
        related='project_id.currency_id',
        string='Currency',
        store=True,
    )
    receipt_attachment = fields.Binary(string='Receipt', attachment=True)
    receipt_filename = fields.Char(string='Receipt Filename')
    notes = fields.Text(string='Notes')

    @api.constrains('amount')
    def _check_amount(self):
        for rec in self:
            if rec.amount < 0:
                raise ValidationError(_('Amount cannot be negative.'))
