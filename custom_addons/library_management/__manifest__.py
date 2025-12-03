# -*- coding: utf-8 -*-
{
    'name': 'Library Management',
    'version': '19.0.2.0.0',
    'category': 'Services/Library',
    'summary': '圖書館管理系統 - 圖書資訊與借閱管理',
    'description': """
圖書館管理系統
==============

本模組提供完整的圖書館管理功能，包括：

核心功能
--------
* 圖書資訊管理（新增、編輯、刪除、查詢）
* 圖書分類系統
* 庫存數量追蹤
* ISBN 格式驗證和唯一性檢查
* 借閱管理（借閱、歸還、續借、取消）
* 自動庫存更新
* 逾期檢查和提醒
* 借閱歷史追蹤
* 多維度搜尋和過濾
* 訊息追蹤功能

借閱功能
--------
* 借閱記錄管理
* 自動計算到期日
* 續借功能（限制次數）
* 逾期天數計算
* 快速借閱按鈕
* 借閱歷史查詢

使用者介面
----------
* 列表視圖 - 快速瀏覽書籍和借閱記錄
* 表單視圖 - 詳細資訊編輯
* 看板視圖 - 視覺化卡片顯示
* 搜尋視圖 - 多維度查詢

權限控制
--------
* Library User - 一般使用者（可查看自己的借閱記錄）
* Library Manager - 圖書管理員（完整權限）

    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        # 安全規則
        'security/library_security.xml',
        'security/ir.model.access.csv',
        
        # 資料
        'data/library_book_category_data.xml',
        'data/library_borrowing_sequence.xml',
        
        # 動作和選單（必須在視圖之前，因為視圖中會參照 action）
        'views/library_menus.xml',
        
        # 視圖
        'views/library_book_category_views.xml',
        'views/library_book_views.xml',
        'views/library_borrowing_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}

