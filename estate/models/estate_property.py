from dateutil.relativedelta import relativedelta

from odoo import models,fields, api



class EstateProperty(models.Model):
    def _default_date_availability(self):
        return fields.Date.context_today(self) + relativedelta(months=3)

    _name = "estate_property"
    _description = "Ma première application"

    
    
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
    garden = fields.Boolean()
    garden_area = fields.Integer()    
    garden_orientation = fields.Selection(
        string = 'Garden Orientation',
        selection = [('north','North'),('south','South'), ('east','East'),('west','West')])
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string = 'State',
        selection = [('new','New'),('offer_received','Offer Received'), ('offer_accepted','Offer Accepted'),('sold','Sold'),('canceled','Canceled')],
        required = True,
        copy = False,
        default = "new",)
    property_type_id = fields.Many2one("estate_property_type", string="Property Type")
    res_partner_id = fields.Many2one("res.partner", string="Buyer")
    res_users_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user, copy=False)
    property_tag_ids = fields.Many2many("estate_property_tag", string="Tag")
    offer_ids = fields.One2many("estate_property_offer", "property_id", string="Offer")
    
    total_area = fields.Integer(compute="_compute_total_area")
    @api.depends('garden_area','living_area')
    def _compute_total_area(self):
        for record in self :
                record.total_area = record.garden_area + record.living_area

    best_price = fields.Integer(compute="_compute_best_price")
    @api.depends('offer_ids.price')
    def _compute_best_price(self) :
        for record in self :
            if record.offer_ids :
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden(self) :
        if self.garden == 1 :
            self.garden_area = 10
            self.garden_orientation = "north"
        else :
            self.garden_area = ""
            self.garden_orientation = ""