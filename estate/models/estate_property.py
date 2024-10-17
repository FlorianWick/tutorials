from dateutil.relativedelta import relativedelta

from odoo import models,fields



class TestModel(models.Model):
    def _default_date_availability(self):
        return fields.Date.context_today(self) + relativedelta(months=3)

    _name = "estate_property"
    _description = "ma première application"

    
    
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date("Available From", default=lambda self: self._default_date_availability(), copy=False)
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
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string = 'State',
        selection = [('new','New'),('offer_received','Offer Received'), ('offer_accepted','Offer Accepted'),('sold','Sold'),('canceled','Canceled')],
        required = True,
        copy = False,
        defaut = "new")
