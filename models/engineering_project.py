from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class EngineeringProject(models.Model):
    _name = 'rgross.engineering.project'
    _description = 'Engineering Project'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'project_code desc'

    name = fields.Char(string='Project Name', required=True, tracking=True)
    project_code = fields.Char(string='Project Code', readonly=True, copy=False, index=True)
    customer_id = fields.Many2one('res.partner', string='Customer', tracking=True)
    project_type = fields.Selection([
        ('mechanical_design', 'Mechanical Design'),
        ('electronics', 'Electronics'),
        ('embedded_systems', 'Embedded Systems'),
        ('simulation', 'Simulation'),
        ('software', 'Software'),
        ('additive_manufacturing', 'Additive Manufacturing'),
        ('automation', 'Automation'),
        ('research', 'Research'),
        ('other', 'Other'),
    ], string='Project Type', tracking=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('waiting_customer', 'Waiting Customer'),
        ('waiting_supplier', 'Waiting Supplier'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)
    priority = fields.Selection([
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ], string='Priority', default='normal')
    start_date = fields.Date(string='Start Date')
    deadline = fields.Date(string='Deadline')
    hourly_rate = fields.Float(string='Hourly Rate (CHF)', default=120.0)
    estimated_hours = fields.Float(string='Estimated Hours')
    real_hours = fields.Float(string='Real Hours')
    material_cost = fields.Monetary(string='Material Cost', currency_field='currency_id')
    external_cost = fields.Monetary(string='External Cost', currency_field='currency_id')
    total_expense_cost = fields.Monetary(
        string='Total Expense Cost',
        compute='_compute_total_expense_cost',
        store=True,
        currency_field='currency_id',
    )
    expected_revenue = fields.Monetary(
        string='Expected Revenue',
        compute='_compute_financials',
        store=True,
        currency_field='currency_id',
    )
    real_service_value = fields.Monetary(
        string='Real Service Value',
        compute='_compute_financials',
        store=True,
        currency_field='currency_id',
    )
    estimated_profit = fields.Monetary(
        string='Estimated Profit',
        compute='_compute_financials',
        store=True,
        currency_field='currency_id',
    )
    real_profit = fields.Monetary(
        string='Real Profit',
        compute='_compute_financials',
        store=True,
        currency_field='currency_id',
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
    )
    description = fields.Html(string='Description')
    technical_notes = fields.Html(string='Technical Notes')
    result_summary = fields.Html(string='Result Summary')
    expense_ids = fields.One2many('rgross.project.expense', 'project_id', string='Expenses')
    expense_count = fields.Integer(string='Expense Count', compute='_compute_expense_count')
    attachment_count = fields.Integer(string='Attachments', compute='_compute_attachment_count')

    @api.depends('expense_ids')
    def _compute_expense_count(self):
        for rec in self:
            rec.expense_count = len(rec.expense_ids)

    @api.depends('expense_ids.amount')
    def _compute_total_expense_cost(self):
        for rec in self:
            rec.total_expense_cost = sum(rec.expense_ids.mapped('amount'))

    @api.depends('estimated_hours', 'real_hours', 'hourly_rate', 'total_expense_cost', 'material_cost', 'external_cost')
    def _compute_financials(self):
        for rec in self:
            rec.expected_revenue = rec.estimated_hours * rec.hourly_rate
            rec.real_service_value = rec.real_hours * rec.hourly_rate
            total_costs = rec.total_expense_cost + rec.material_cost + rec.external_cost
            rec.estimated_profit = rec.expected_revenue - total_costs
            rec.real_profit = rec.real_service_value - total_costs

    def _compute_attachment_count(self):
        for rec in self:
            rec.attachment_count = self.env['ir.attachment'].search_count([
                ('res_model', '=', self._name),
                ('res_id', '=', rec.id),
            ])

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('project_code'):
                vals['project_code'] = self.env['ir.sequence'].next_by_code('rgross.engineering.project') or '/'
        return super().create(vals_list)

    @api.constrains('hourly_rate', 'estimated_hours', 'real_hours')
    def _check_positive_values(self):
        for rec in self:
            if rec.hourly_rate < 0:
                raise ValidationError(_('Hourly rate cannot be negative.'))
            if rec.estimated_hours < 0:
                raise ValidationError(_('Estimated hours cannot be negative.'))
            if rec.real_hours < 0:
                raise ValidationError(_('Real hours cannot be negative.'))

    @api.constrains('start_date', 'deadline')
    def _check_dates(self):
        for rec in self:
            if rec.start_date and rec.deadline and rec.deadline < rec.start_date:
                raise ValidationError(_('Deadline cannot be earlier than start date.'))

    def action_set_active(self):
        self.write({'status': 'active'})

    def action_set_waiting_customer(self):
        self.write({'status': 'waiting_customer'})

    def action_set_waiting_supplier(self):
        self.write({'status': 'waiting_supplier'})

    def action_set_done(self):
        self.write({'status': 'done'})

    def action_cancel(self):
        self.write({'status': 'cancelled'})

    def action_reset_draft(self):
        self.write({'status': 'draft'})

    def action_view_expenses(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Expenses'),
            'res_model': 'rgross.project.expense',
            'view_mode': 'list,form',
            'domain': [('project_id', '=', self.id)],
            'context': {'default_project_id': self.id},
        }

    def action_view_attachments(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Attachments'),
            'res_model': 'ir.attachment',
            'view_mode': 'list,form',
            'domain': [('res_model', '=', self._name), ('res_id', '=', self.id)],
            'context': {'default_res_model': self._name, 'default_res_id': self.id},
        }
