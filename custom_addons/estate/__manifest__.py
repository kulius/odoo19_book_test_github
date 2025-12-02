 {
    'name': "Real Estate",
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',        
        'views/estate_property_tag_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',        
        'views/estate_menus.xml',
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',
    ],
    'application': True,
}