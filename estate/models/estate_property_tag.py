from odoo import models,fields



class EstatePropertyTag(models.Model):

    _name = "estate_property_tag"
    _description = "Classification des propriétés"
    
    _sql_constraints = [
        ("unique_tag_name","UNIQUE(name)", "Il ne peut pas y avoir 2 tags identiques banane"),
    ]
    
    _order = "name"
    name = fields.Char(required=True)
    color = fields.Integer()