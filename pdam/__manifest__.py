# -*- coding: utf-8 -*-
{
    'name': "PDAM",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'account', 'stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'data/ir_cron.xml',
        # 'data/mail_template.xml',
        'views/res_partner_views.xml',
        'views/pdam_management_views.xml',
        'views/menus.xml',
        'views/account_move_views.xml',
        'wizard/import_data_pelanggan/import_customer_data_view.xml',
        'wizard/whatsapp_send_message.xml',
        # 'reports/report_action.xml',
        'reports/pdam_report_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
