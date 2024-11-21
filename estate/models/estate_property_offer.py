from dateutil.relativedelta import relativedelta

from odoo import models,fields



class EstatePropertyOffers(models.Model):

    _name = "estate_property_offer"
    _description = "Offres d'achat"
    
    
    price = fields.Float(required=True, string="Price")
    status = fields.Selection(
        string = 'Statut',
        selection = [('accepted','Accepted'),('refused','Refused')],)
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate_property", string="Property", required=True)