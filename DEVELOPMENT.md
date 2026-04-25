# Development Guide

This guide covers how to extend and customize the **RGross Engineering Hub** module.

---

## Project Structure

```
rgross_engineering_hub/
├── __init__.py                      # Module initialization
├── __manifest__.py                  # Module metadata
├── data/
│   └── sequence.xml                 # ENG- sequence definition
├── models/
│   ├── __init__.py                  # Models loader
│   ├── engineering_project.py       # Main project model
│   └── project_expense.py           # Expense model
├── security/
│   └── ir.model.access.csv          # Access control rules
└── views/
    ├── engineering_project_views.xml # Project views (list, form, kanban, etc.)
    ├── project_expense_views.xml     # Expense views
    └── menu.xml                      # Menu structure
```

---

## Adding New Fields

### To `rgross.engineering.project`:

Edit `models/engineering_project.py`:

```python
from odoo import api, fields, models

class EngineeringProject(models.Model):
    _name = 'rgross.engineering.project'
    
    # Add new field
    new_field = fields.Char(string='My New Field', required=True)
    
    # Computed field example
    computed_field = fields.Float(compute='_compute_something', store=True)
    
    @api.depends('some_field')
    def _compute_something(self):
        for rec in self:
            rec.computed_field = rec.some_field * 2
```

Then add the field to the form in `views/engineering_project_views.xml`:

```xml
<field name="new_field"/>
```

---

## Adding New Views

### Example: Add a Report View

Create a new file `views/project_report_views.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_rgross_engineering_project_report" model="ir.ui.view">
        <field name="name">rgross.engineering.project.report</field>
        <field name="model">rgross.engineering.project</field>
        <field name="arch" type="xml">
            <graph string="Project Profitability" type="line">
                <field name="create_date" interval="week"/>
                <field name="real_profit" type="measure"/>
            </graph>
        </field>
    </record>
</odoo>
```

Add to `__manifest__.py`:

```python
'data': [
    # ... existing files
    'views/project_report_views.xml',
]
```

---

## Adding Custom Methods

### Action Methods

In `models/engineering_project.py`:

```python
def action_send_email(self):
    """Send project summary to customer"""
    for rec in self:
        # Your logic here
        pass
    return {'type': 'ir.actions.act_window_close'}
```

Add button to form:

```xml
<button name="action_send_email" string="Send Email" type="object" class="btn-primary"/>
```

### Compute Methods

```python
@api.depends('expense_ids.amount', 'material_cost')
def _compute_total_cost(self):
    for rec in self:
        rec.total_cost = sum(rec.expense_ids.mapped('amount')) + rec.material_cost
```

---

## Extending Models

### Inherit and Extend

Create a new module `rgross_engineering_hub_extended/` that extends the base module:

```python
# models/engineering_project_extended.py
from odoo import fields, models

class EngineeringProjectExtended(models.Model):
    _inherit = 'rgross.engineering.project'
    
    custom_field = fields.Char(string='Custom Field')
```

In `__manifest__.py`:

```python
'depends': ['rgross_engineering_hub'],  # Depend on base module
```

---

## Database Migrations

### Adding a new field with existing data

In Odoo, fields are created automatically. But for complex migrations:

1. Create a Python migration file (optional)
2. Add a `post_init_hook` in `__manifest__.py`

```python
def post_init_hook(cr, registry):
    """Run after module installation"""
    # Migration logic
    pass

'post_init_hook': 'post_init_hook',
```

---

## Testing

### Basic Model Test

Create `tests/test_engineering_project.py`:

```python
from odoo.tests import TransactionCase

class TestEngineeringProject(TransactionCase):
    def setUp(self):
        super().setUp()
        self.project = self.env['rgross.engineering.project'].create({
            'name': 'Test Project',
        })
    
    def test_project_creation(self):
        self.assertTrue(self.project.id)
        self.assertTrue(self.project.project_code.startswith('ENG-'))
    
    def test_profit_calculation(self):
        self.project.estimated_hours = 10
        self.project.hourly_rate = 100
        expected = 1000
        self.assertEqual(self.project.expected_revenue, expected)
```

Run tests:

```bash
cd /opt/odoo
./odoo-bin -d RGross -i rgross_engineering_hub --test-enable --stop-after-init
```

---

## API Usage

### Creating a Project via API

```python
# In your code
project = self.env['rgross.engineering.project'].create({
    'name': 'My Project',
    'customer_id': 2,  # Partner ID
    'project_type': 'mechanical_design',
    'status': 'draft',
    'hourly_rate': 150.0,
})

# Project code is auto-generated
print(project.project_code)  # ENG-0001
```

### Adding an Expense

```python
expense = self.env['rgross.project.expense'].create({
    'name': 'Steel parts',
    'project_id': project.id,
    'expense_type': 'material',
    'amount': 500.00,
    'vendor_id': 5,  # Partner ID
})
```

### Fetching Data

```python
# Get all active projects
active_projects = self.env['rgross.engineering.project'].search([
    ('status', '=', 'active')
])

# Get profitable projects
profitable = self.env['rgross.engineering.project'].search([
    ('real_profit', '>', 0)
])

# Get project with expenses
project = self.env['rgross.engineering.project'].browse(1)
total_expenses = sum(project.expense_ids.mapped('amount'))
```

---

## Common Customizations

### 1. Add a New Expense Type

Edit `models/project_expense.py`:

```python
expense_type = fields.Selection([
    ('material', 'Material'),
    ('consulting', 'Consulting'),  # NEW
    # ...
], string='Expense Type')
```

### 2. Add Project Status

Edit `models/engineering_project.py`:

```python
status = fields.Selection([
    ('draft', 'Draft'),
    ('in_review', 'In Review'),  # NEW
    # ...
], string='Status')
```

### 3. Add Email Notification on Status Change

```python
def write(self, vals):
    if 'status' in vals and vals['status'] == 'done':
        # Send email
        self.send_completion_email()
    return super().write(vals)
```

---

## Debugging

### Enable Logging

In `__manifest__.py` or Python code:

```python
import logging
logger = logging.getLogger(__name__)

# In methods:
logger.info(f'Project {self.name} created')
logger.warning(f'High profit: {self.real_profit}')
logger.error('Something went wrong')
```

View logs:

```bash
tail -f /var/log/odoo/odoo.log | grep rgross_engineering
```

### Python Debugger

In your method:

```python
def compute_profit(self):
    import pdb; pdb.set_trace()  # Breakpoint
    profit = self.real_service_value - self.total_expense_cost
    return profit
```

Then run Odoo in foreground and interact with the debugger.

---

## Contributing

1. Fork the [GitHub repository](https://github.com/rafaeltgross/rgross_engineering_hub)
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make changes and test
4. Commit: `git commit -am 'Add my feature'`
5. Push: `git push origin feature/my-feature`
6. Create a Pull Request

---

## Resources

- [Odoo 19 Documentation](https://www.odoo.com/documentation/19.0/)
- [Odoo Developer Guide](https://www.odoo.com/documentation/19.0/developer.html)
- [XML View Architecture](https://www.odoo.com/documentation/19.0/developer/reference/backend/views.html)
