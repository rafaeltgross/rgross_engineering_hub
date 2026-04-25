{
    'name': 'RGross Engineering Hub',
    'version': '19.0.1.0.0',
    'category': 'Project',
    'summary': 'Engineering Project & Expense Hub for Swiss engineering/R&D companies',
    'author': 'RGross',
    'depends': ['base', 'mail', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/engineering_project_views.xml',
        'views/project_expense_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
