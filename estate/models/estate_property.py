from odoo import models,fields

def _default_date_availability(self):
        return 

class TestModel(models.Model):
    _name = "estate_property"
    _description = "ma première application"
    
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=fields.Date.context_today(self) + relativedelta(months=3),copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer(default="2")
    living_area = fields.Integer()
    facades = fields.Boolean()
    garage = fields.Boolean()
    garden_area = fields.Integer    
    garden_orientation = fields.Selection(
        string = 'Garden Orientation',
        selection = [('north','North'),('south','South'), ('east','East'),('west','West')]) 
