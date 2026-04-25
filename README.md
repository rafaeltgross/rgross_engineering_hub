# RGross Engineering Hub

Odoo 19 Community custom module — **Engineering Project & Expense Hub** for a Swiss engineering/R&D company.

---

## Features

### Engineering Projects (`rgross.engineering.project`)
- Auto-generated project codes (`ENG-0001`, `ENG-0002`, …)
- Project types: Mechanical Design, Electronics, Embedded Systems, Simulation, Software, Additive Manufacturing, Automation, Research
- Full lifecycle status: Draft → Active → Waiting Customer / Waiting Supplier → Done / Cancelled
- Priority levels: Low, Normal, High, Urgent
- Financial tracking:
  - Hourly rate × estimated/real hours
  - Material and external costs
  - Aggregated expense costs (from linked expenses)
  - Estimated and real profit
- Rich-text fields: Description, Technical Notes, Result Summary
- Chatter (mail.thread) + Activities (mail.activity.mixin)
- Smart buttons for Expenses and Attachments

### Project Expenses (`rgross.project.expense`)
- Expense types: Material, Electronic Component, 3D Printing, Prototype, Software License, Supplier Service, Travel, Shipping, Other
- Vendor tracking
- Binary receipt attachment
- Cascaded to parent project

### Views
| Model | Views |
|---|---|
| Engineering Project | List, Form, Kanban (grouped by status), Graph, Pivot |
| Project Expense | List, Form, Graph, Pivot |

### Menu
```
RGross Engineering
├── Projects
├── Expenses
└── Customers
```

---

## Installation

### Requirements
- Odoo **19.0 Community Edition**
- Dependencies: `base`, `mail`, `contacts`

### Steps

```bash
# 1. Copy to addons path
cp -r rgross_engineering_hub /opt/odoo/custom-addons/

# 2. Fix ownership
chown -R odoo:odoo /opt/odoo/custom-addons/rgross_engineering_hub

# 3. Restart Odoo
systemctl restart odoo
```

Then in the Odoo web interface:

1. Enable **Developer Mode** → Settings → Activate developer mode
2. Go to **Apps** → click **Update Apps List**
3. Search for `RGross Engineering Hub`
4. Click **Install**

---

## Module Structure

```
rgross_engineering_hub/
├── __init__.py
├── __manifest__.py
├── data/
│   └── sequence.xml               # ENG- sequence
├── models/
│   ├── __init__.py
│   ├── engineering_project.py     # rgross.engineering.project
│   └── project_expense.py         # rgross.project.expense
├── security/
│   └── ir.model.access.csv        # Access rights for base users
└── views/
    ├── engineering_project_views.xml
    ├── project_expense_views.xml
    └── menu.xml
```

---

## Data Model

### `rgross.engineering.project`

| Field | Type | Description |
|---|---|---|
| `project_code` | Char (readonly) | Auto-generated: `ENG-0001` |
| `name` | Char | Project name |
| `customer_id` | Many2one `res.partner` | Customer |
| `project_type` | Selection | Type of engineering work |
| `status` | Selection | Lifecycle status |
| `priority` | Selection | Low / Normal / High / Urgent |
| `start_date` / `deadline` | Date | Timeline |
| `hourly_rate` | Float | Billing rate (CHF) |
| `estimated_hours` / `real_hours` | Float | Time tracking |
| `material_cost` / `external_cost` | Monetary | Direct costs |
| `total_expense_cost` | Monetary (computed) | Sum of all linked expenses |
| `expected_revenue` | Monetary (computed) | `estimated_hours × hourly_rate` |
| `real_service_value` | Monetary (computed) | `real_hours × hourly_rate` |
| `estimated_profit` / `real_profit` | Monetary (computed) | Revenue minus all costs |
| `description` | Html | Project description |
| `technical_notes` | Html | Internal technical notes |
| `result_summary` | Html | Final results |

### `rgross.project.expense`

| Field | Type | Description |
|---|---|---|
| `name` | Char | Expense label |
| `project_id` | Many2one | Parent project (cascade delete) |
| `date` | Date | Expense date |
| `expense_type` | Selection | Category |
| `vendor_id` | Many2one `res.partner` | Supplier |
| `amount` | Monetary | Cost |
| `receipt_attachment` | Binary | Scanned receipt |
| `notes` | Text | Additional notes |

---

## Company Context

Built for a Swiss engineering/R&D company offering:
- Mechanical design (SolidWorks)
- Embedded systems (ESP32)
- Electronics and PCB prototyping
- 3D printing / additive manufacturing
- Mechanical and thermal simulation
- Automation and software development
- R&D prototypes (bee counters, oxalic acid fumigators, pellet 3D printers, energy harvesting, energy meters)

---

## License

LGPL-3
