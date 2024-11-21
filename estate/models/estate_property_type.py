from odoo import models,fields



class EstatePropertyType(models.Model):

    _name = "estate_property_type"
    _description = "Types de propriétés"
    
    
    name = fields.Char(required=True)