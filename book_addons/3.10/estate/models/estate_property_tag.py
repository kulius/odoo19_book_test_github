# in estate/models/estate_property_tag.py
from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    
    _unique_name = models.Constraint(
    'UNIQUE(name)',
    'A property tag name must be unique.',)

    name = fields.Char(required=True)
    