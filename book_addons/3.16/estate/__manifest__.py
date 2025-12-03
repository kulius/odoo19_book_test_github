{
   'name': "Real Estate",
   'depends': [
       'base',
   ],
   'data': [
       # 安全性設定 (必須先載入群組定義)
       'security/estate_security.xml',
       'security/ir.model.access.csv',
       # 視圖
       'views/estate_property_tag_views.xml',
       'views/estate_property_views.xml',
       'views/estate_property_type_views.xml',        
       'views/estate_menus.xml',
       # 報表
       'report/estate_property_templates.xml',
       'report/estate_property_reports.xml',
   ],
   'application': True,
   'category': 'Real Estate',
}