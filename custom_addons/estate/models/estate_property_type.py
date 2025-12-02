from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name" # 新增這一行

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'A property type name must be unique.',
    )

    sequence = fields.Integer('Sequence', default=10)
    name = fields.Char(required=True)
    # 新增下面這行
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")

    property_count = fields.Integer(compute='_compute_property_count')

    def _compute_property_count(self):
        for record in self:
            # Odoo 會自動處理 One2many 的計數
            record.property_count = len(record.property_ids)
