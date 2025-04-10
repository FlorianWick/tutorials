from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError

from odoo import models,fields,api


class EstatePropertyOffers(models.Model):

    _name = "estate_property_offer"
    _description = "Offres"
    description = fields.Char(compute="_compute_description", store=True)
    
     ###Sql contraints
    _sql_constraints = [
        ("check_expected_price","CHECK(price > 0)", "Merci de ne pas donner nos biens et vérifier votre offre !"),
    ]

    ##Order
    _order = "price desc"

    price = fields.Float(required=True, string="Price")
    status = fields.Selection(
        string = 'Statut',
        selection = [('accepted','Accepted'),('refused','Refused')],)
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate_property", string="Property", required=True)
    validity = fields.Integer(default=7, string="Validity")

    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline")
    property_type_id = fields.Many2one("estate_property_type", related="property_id.property_type_id", string="Property Type", store=True)
    
    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - date).days

    @api.depends("partner_id.name")
    def _compute_description(self):
        for record in self:
            record.description = "Test for partner %s" % record.partner_id.name
            
  ### Action
    def action_accept_property_offer(self):
        if "accepted" in self.mapped("property_id.offer_ids.status"):
            raise ValidationError("Une offre a déjà été acceptée pour cette propriétée")
        self.status = "accepted"
        self.property_id.write ({
            "state" : "offer_accepted",
            "selling_price" : self.price,
            "res_partner_id" : self.partner_id,
        })
    
    def action_refuse_property_offer(self):
        self.status = "refused"