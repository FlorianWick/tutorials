from odoo import models,fields



class EstatePropertyTag(models.Model):

    _name = "estate_property_tag"
    _description = "Classification des propriétés"
    
    
    name = fields.Char(required=True)