# API Reference

Complete reference for the **RGross Engineering Hub** models and fields.

---

## Models

### `rgross.engineering.project`

Main model for engineering projects.

**Inheritance:** `mail.thread`, `mail.activity.mixin`

#### Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | Integer | Auto | Unique identifier |
| `project_code` | Char | Readonly | Auto-generated code (ENG-0001) |
| `name` | Char | **Yes** | Project name |
| `customer_id` | Many2one | No | Link to res.partner (customer) |
| `project_type` | Selection | No | Type of work (see values below) |
| `status` | Selection | No | Current status (draft, active, …) |
| `priority` | Selection | No | Priority level (low, normal, high, urgent) |
| `start_date` | Date | No | Project start date |
| `deadline` | Date | No | Project deadline |
| `hourly_rate` | Float | No | Billing rate in CHF (default: 120.0) |
| `estimated_hours` | Float | No | Estimated labor hours |
| `real_hours` | Float | No | Actual labor hours |
| `material_cost` | Monetary | No | Direct material costs |
| `external_cost` | Monetary | No | External service costs |
| `total_expense_cost` | Monetary | Computed | Sum of all expenses |
| `expected_revenue` | Monetary | Computed | `estimated_hours × hourly_rate` |
| `real_service_value` | Monetary | Computed | `real_hours × hourly_rate` |
| `estimated_profit` | Monetary | Computed | Expected revenue minus costs |
| `real_profit` | Monetary | Computed | Real revenue minus costs |
| `currency_id` | Many2one | No | Currency (default: company currency) |
| `description` | Html | No | Project description |
| `technical_notes` | Html | No | Technical notes |
| `result_summary` | Html | No | Final results summary |
| `expense_ids` | One2many | No | Related expenses (rgross.project.expense) |
| `expense_count` | Integer | Computed | Number of linked expenses |
| `attachment_count` | Integer | Computed | Number of attachments |
| `create_date` | Datetime | Auto | Created on |
| `write_date` | Datetime | Auto | Last modified |
| `create_uid` | Many2one | Auto | Created by (res.users) |
| `write_uid` | Many2one | Auto | Modified by (res.users) |

#### Selection Values

**`project_type`:**
- `mechanical_design` — Mechanical Design
- `electronics` — Electronics
- `embedded_systems` — Embedded Systems
- `simulation` — Simulation
- `software` — Software
- `additive_manufacturing` — Additive Manufacturing
- `automation` — Automation
- `research` — Research
- `other` — Other

**`status`:**
- `draft` — Draft
- `active` — Active
- `waiting_customer` — Waiting Customer
- `waiting_supplier` — Waiting Supplier
- `done` — Done
- `cancelled` — Cancelled

**`priority`:**
- `low` — Low
- `normal` — Normal
- `high` — High
- `urgent` — Urgent

#### Methods

##### Actions (for buttons)

```python
def action_set_active(self)
    """Change status to active"""
    
def action_set_waiting_customer(self)
    """Change status to waiting_customer"""
    
def action_set_waiting_supplier(self)
    """Change status to waiting_supplier"""
    
def action_set_done(self)
    """Change status to done"""
    
def action_cancel(self)
    """Change status to cancelled"""
    
def action_reset_draft(self)
    """Reset status to draft"""
```

##### View Actions

```python
def action_view_expenses(self)
    """Open linked expenses in a new window"""
    
def action_view_attachments(self)
    """Open linked attachments in a new window"""
```

#### Computed Fields

**`total_expense_cost`**
```
Depends on: expense_ids.amount
Value = SUM(expense_ids.amount)
```

**`expected_revenue`**
```
Depends on: estimated_hours, hourly_rate
Value = estimated_hours × hourly_rate
```

**`real_service_value`**
```
Depends on: real_hours, hourly_rate
Value = real_hours × hourly_rate
```

**`estimated_profit`**
```
Depends on: expected_revenue, total_expense_cost, material_cost, external_cost
Value = expected_revenue - (total_expense_cost + material_cost + external_cost)
```

**`real_profit`**
```
Depends on: real_service_value, total_expense_cost, material_cost, external_cost
Value = real_service_value - (total_expense_cost + material_cost + external_cost)
```

#### Constraints

- `hourly_rate >= 0` (cannot be negative)
- `estimated_hours >= 0` (cannot be negative)
- `real_hours >= 0` (cannot be negative)
- `deadline >= start_date` (deadline cannot be before start date)

#### Sequence

Automatically generates `project_code` on creation using sequence `rgross.engineering.project`:
- Prefix: `ENG-`
- Format: `ENG-0001, ENG-0002, …`

---

### `rgross.project.expense`

Model for tracking project expenses.

#### Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | Integer | Auto | Unique identifier |
| `name` | Char | **Yes** | Expense description |
| `project_id` | Many2one | **Yes** | Parent project (cascade delete) |
| `date` | Date | No | Expense date (default: today) |
| `expense_type` | Selection | No | Type of expense |
| `vendor_id` | Many2one | No | Supplier/vendor (res.partner) |
| `amount` | Monetary | No | Expense amount |
| `currency_id` | Many2one | Related | Currency (from project) |
| `receipt_attachment` | Binary | No | Receipt file (PDF, image, etc.) |
| `receipt_filename` | Char | No | Original filename of receipt |
| `notes` | Text | No | Additional notes |
| `create_date` | Datetime | Auto | Created on |
| `write_date` | Datetime | Auto | Last modified |

#### Selection Values

**`expense_type`:**
- `material` — Material
- `electronic_component` — Electronic Component
- `3d_printing` — 3D Printing
- `prototype` — Prototype
- `software_license` — Software License
- `supplier_service` — Supplier Service
- `travel` — Travel
- `shipping` — Shipping
- `other` — Other

#### Constraints

- `amount >= 0` (cannot be negative)

---

## API Examples

### Create a Project

```python
project = env['rgross.engineering.project'].create({
    'name': 'SolidWorks Design - New Product',
    'customer_id': 15,
    'project_type': 'mechanical_design',
    'status': 'active',
    'priority': 'high',
    'start_date': '2026-04-01',
    'deadline': '2026-05-31',
    'hourly_rate': 150.0,
    'estimated_hours': 40.0,
})

print(project.project_code)  # ENG-0001
```

### Create an Expense

```python
expense = env['rgross.project.expense'].create({
    'name': 'Stainless steel plates',
    'project_id': project.id,
    'date': '2026-04-15',
    'expense_type': 'material',
    'vendor_id': 42,
    'amount': 450.50,
    'notes': 'For prototype testing',
})
```

### Update Project Hours

```python
project.write({
    'real_hours': 35.5,
    'status': 'waiting_customer',
})

# Profit is auto-computed
print(f"Real Profit: CHF {project.real_profit}")
```

### Search Active Projects

```python
active_projects = env['rgross.engineering.project'].search([
    ('status', '=', 'active'),
])

for proj in active_projects:
    print(f"{proj.project_code}: {proj.name} - {proj.real_profit} CHF profit")
```

### Get Expensive Projects

```python
expensive = env['rgross.engineering.project'].search([
    ('total_expense_cost', '>', 1000),
])
```

### Get Expenses for a Project

```python
project = env['rgross.engineering.project'].browse(1)

for expense in project.expense_ids:
    print(f"{expense.name}: {expense.amount}")

total = project.total_expense_cost
print(f"Total Expenses: {total}")
```

### Filter by Project Type

```python
electronics_projects = env['rgross.engineering.project'].search([
    ('project_type', 'in', ['electronics', 'embedded_systems']),
])
```

### Get Projects Overdue

```python
from odoo import fields

overdue = env['rgross.engineering.project'].search([
    ('deadline', '<', fields.Date.today()),
    ('status', '!=', 'done'),
])
```

---

## Access Control

Both models have full read/write/create/delete permissions for `base.group_user` (regular users).

To restrict access, modify `security/ir.model.access.csv`:

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_rgross_engineering_project_manager,rgross.engineering.project.manager,model_rgross_engineering_project,my_group_manager,1,1,1,1
access_rgross_engineering_project_user,rgross.engineering.project.user,model_rgross_engineering_project,base.group_user,1,0,0,0
```

This makes read-only for regular users, edit for managers.

---

## Mail & Activities

Because `rgross.engineering.project` inherits `mail.thread` and `mail.activity.mixin`:

### Chatter

```python
project.message_post(
    body="Project is delayed",
    message_type='comment',
)
```

### Activities

```python
activity = project.activity_schedule(
    activity_type_xmlid='mail.mail_activity_data_call',
    summary='Call customer',
    user_id=env.user.id,
)
```

---

## Reports & Analytics

### Graph View (Profit by Project Type)

Available in the Projects list view.

### Pivot View (Complex Analysis)

Create custom pivots in the UI:
- Rows: Project Type, Status
- Cols: Priority
- Measures: Real Profit, Real Hours, Total Expense Cost

### Kanban View

Grouped by status:
- **Draft**
- **Active**
- **Waiting Customer**
- **Waiting Supplier**
- **Done**
- **Cancelled**

---

## Webhooks & Events

To react to changes, override the `write()` method:

```python
def write(self, vals):
    # Before writing
    if 'status' in vals and vals['status'] == 'done':
        self._on_project_done()
    
    result = super().write(vals)
    
    # After writing
    if 'real_hours' in vals:
        self._notify_hours_updated()
    
    return result

def _on_project_done(self):
    """Called when status changes to done"""
    self.message_post(body="Project completed!")
```

---

## Performance Tips

1. Use `search()` with indexed fields (`project_code`, `status`)
2. Use `mapped()` for bulk operations: `expenses.mapped('amount')`
3. Avoid N+1 queries: use `prefetch_related()` or join loads
4. Cache computed fields with `store=True`

---

For more information, see [DEVELOPMENT.md](DEVELOPMENT.md) or the [Odoo 19 Documentation](https://www.odoo.com/documentation/19.0/).
