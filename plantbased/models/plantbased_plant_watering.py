from odoo import models, fields

class Watering(models.Model):

    #---------------------------------DESCRIPTION---------------------------------#
    _name = 'plantbased_plant_watering'
    _description = 'Arrosages'

    #---------------------------------BASIC FIELDS---------------------------------#
    date = fields.Date(string="Date d'arrosage", required=True, default=fields.Date.today)
    volume = fields.Selection([
        ('low', 'Bas'),
        ('medium', 'Moyen'),
        ('high', 'Fort')
    ], string="Quantité", required=True, default='medium')
    plant_health = fields.Selection([
        ('healthy', "En bonne santé"),
        ('not_that_healthy', "Bof bof la santé"),
        ('not_healthy', "En train de die")
    ], string="Santé de la plante", required=True, default='healthy')
    photo = fields.Image()
    #---------------------------------RELATIONNAL FIELDS---------------------------------#
    plant_id = fields.Many2one('plantbased_plant', string="Plante", required=True)