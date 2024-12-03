from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta

from odoo import models,fields,api

import logging

_logger = logging.getLogger(__name__)

class EstatePropertyOffers(models.Model):

    _name = "estate_property_offer"
    description = fields.Char(compute="_compute_description", store=True)
    
    
    price = fields.Float(required=True, string="Price")
    status = fields.Selection(
        string = 'Statut',
        selection = [('accepted','Accepted'),('refused','Refused')],)
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate_property", string="Property", required=True)
    validity = fields.Integer(default=7, string="Validity")

    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline")
    
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
            
