# Changelog

All notable changes to **RGross Engineering Hub** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [19.0.1.0.0] — 2026-04-25

### Added

#### Models
- **`rgross.engineering.project`** — Main engineering project tracking model
  - Auto-generated project codes (ENG-0001, ENG-0002, …)
  - 9 project types: Mechanical Design, Electronics, Embedded Systems, Simulation, Software, Additive Manufacturing, Automation, Research, Other
  - 6 status levels: Draft, Active, Waiting Customer, Waiting Supplier, Done, Cancelled
  - Priority levels: Low, Normal, High, Urgent
  - Financial tracking: Hourly rate, estimated/real hours, costs, profit calculation
  - Rich-text fields: Description, Technical Notes, Result Summary
  - Integrated chatter (mail.thread) and activities (mail.activity.mixin)

- **`rgross.project.expense`** — Project expense tracking
  - 9 expense types: Material, Electronic Component, 3D Printing, Prototype, Software License, Supplier Service, Travel, Shipping, Other
  - Vendor/supplier tracking
  - Receipt attachment support
  - Cascaded to parent project

#### Features
- **Financial Tracking**
  - Hourly rate × hours = Service value
  - Aggregated expense costs from linked expenses
  - Estimated vs. real profit calculation
  - Full monetary field support with multi-currency

- **Views**
  - List view with essential columns and decorations
  - Form view with header, statusbar, smart buttons, groups, notebook tabs
  - Kanban view grouped by status
  - Graph view for profit analysis
  - Pivot view for complex analysis
  - Search view with filters and grouping options

- **Menu Structure**
  - RGross Engineering (root menu)
    - Projects (main CRUD)
    - Expenses (secondary CRUD)
    - Customers (link to contacts)

- **Smart Buttons**
  - Expenses counter and action
  - Attachments counter and action

- **Status Workflow**
  - Set Active, Set Waiting Customer, Set Waiting Supplier, Set Done, Cancel, Reset to Draft

- **Automation**
  - Auto-generate project codes via sequence
  - Auto-compute financial fields
  - Constraint validation (positive values, date logic)

#### Documentation
- Comprehensive README.md
- Installation guide (INSTALL.md)
- Development guide (DEVELOPMENT.md)
- API reference (API.md)
- This changelog

### Technical
- Odoo 19 Community Edition compatibility
- Minimal dependencies: base, mail, contacts
- Full access control (base.group_user)
- Sequence auto-increment with ENG- prefix, 4-digit padding
- Mail integration for chatter and activities
- Computed fields with proper dependency tracking

---

## Future Roadmap

### [19.0.2.0.0] — Planned
- PDF report generation for projects
- Email notifications on status changes
- Expense approval workflow
- Integration with account_accountant for billable expenses
- Time tracking via timesheets
- Customer portal view

### [19.0.3.0.0] — Planned
- Analytics dashboard
- Project templates
- Recurring expense rules
- Mobile app support
- Multi-language support (i18n)

---

## Installation & Support

- **Installation:** See [INSTALL.md](INSTALL.md)
- **Development:** See [DEVELOPMENT.md](DEVELOPMENT.md)
- **API Reference:** See [API.md](API.md)
- **GitHub:** [rafaeltgross/rgross_engineering_hub](https://github.com/rafaeltgross/rgross_engineering_hub)

---

## License

LGPL-3 — See [LICENSE](LICENSE) file.
