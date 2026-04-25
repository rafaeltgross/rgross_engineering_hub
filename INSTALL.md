# Installation Guide

## Prerequisites

- **Odoo 19.0 Community Edition**
- Python 3.8+
- PostgreSQL 12+
- Linux/macOS (or WSL on Windows)

### Dependencies

The module depends on:
- `base` — Odoo base module
- `mail` — Chatter and mail features
- `contacts` — res.partner model

These are included in all Odoo installations.

---

## Step 1: Copy the Module

```bash
cp -r rgross_engineering_hub /opt/odoo/custom-addons/
```

Or clone from GitHub:

```bash
cd /opt/odoo/custom-addons
git clone https://github.com/rafaeltgross/rgross_engineering_hub.git
```

---

## Step 2: Fix Ownership

```bash
chown -R odoo:odoo /opt/odoo/custom-addons/rgross_engineering_hub/
```

Replace `odoo` with your actual Odoo user if different.

---

## Step 3: Restart Odoo

```bash
systemctl restart odoo
```

Or if using a different service manager:

```bash
sudo service odoo restart
```

For development mode (with auto-reload):

```bash
cd /opt/odoo && ./odoo-bin -c /etc/odoo.conf -d RGross --dev=all
```

---

## Step 4: Update Apps List in Odoo Web

1. Log in to Odoo as Administrator
2. **Settings** → **Activate Developer Mode** (in top-right corner)
3. **Apps** → **Update Apps List** (blue button, top-right)
4. Wait for the update to complete

---

## Step 5: Install the Module

1. **Apps** (stay in the Apps menu)
2. **Clear the search** (if it's filtered)
3. Search for `RGross Engineering`
4. Click **RGross Engineering Hub**
5. Click **Install**

---

## Step 6: Verify Installation

After installation:

1. **RGross Engineering** menu should appear in the sidebar
2. Click **Projects** → Should open an empty project list
3. Click **Expenses** → Should open an empty expense list

If you see these menus, installation is complete ✓

---

## Troubleshooting

### Module not appearing in Apps list

**Solution:**
```bash
# Force reload Odoo modules
systemctl restart odoo

# Check logs
tail -f /var/log/odoo/odoo.log
```

### Permission denied error

**Solution:**
```bash
# Check ownership
ls -la /opt/odoo/custom-addons/rgross_engineering_hub/

# Fix if needed
sudo chown -R odoo:odoo /opt/odoo/custom-addons/rgross_engineering_hub/

# Restart
systemctl restart odoo
```

### "Model not found" error

This usually means the module didn't fully load. Check:

```bash
# Check for Python syntax errors
python3 -m py_compile /opt/odoo/custom-addons/rgross_engineering_hub/models/*.py

# Check XML syntax
python3 -c "import xml.etree.ElementTree as ET; ET.parse('/opt/odoo/custom-addons/rgross_engineering_hub/views/menu.xml')"
```

### Database errors after install

The module auto-creates sequences and tables. If you see database errors:

1. Deinstall the module
2. Restart Odoo
3. Re-install the module

---

## Multi-Database Setup

If you have multiple Odoo databases, install on each database separately:

1. Switch to the desired database in Odoo (top-right selector)
2. Go to **Apps** → Search → Install

The module will be database-independent.

---

## Uninstallation

To remove the module:

1. **Apps** → Search `RGross Engineering`
2. Click the module
3. Click **Uninstall**
4. Delete the folder: `rm -rf /opt/odoo/custom-addons/rgross_engineering_hub`
5. Restart Odoo

**Note:** Uninstalling will delete all project and expense records created in this module.

---

## Support

For issues, check the [README.md](README.md) or the [GitHub repository](https://github.com/rafaeltgross/rgross_engineering_hub).
