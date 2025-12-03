# -*- coding: utf-8 -*-
{
    'name': 'Sale Account Custom',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': '銷售訂單自訂欄位 - 運送備註與應收帳款總金額',
    'description': """
        銷售訂單擴展功能
        =================
        * 新增運送備註欄位
        * 新增計算會計應收總金額欄位
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': [
        'sale',
        'account',
    ],
    'data': [
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}

