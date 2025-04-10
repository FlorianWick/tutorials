from odoo import models, fields

class Species(models.Model):

    #---------------------------------DESCRIPTION---------------------------------#
    _name = 'plantbased_plant_species'
    _description = 'Espèce plante'

    #---------------------------------BASIC FIELDS---------------------------------#
    name = fields.Char(string="Nom", required=True)
    description = fields.Text(string="Description")
    watering_frequency_summer = fields.Integer(string="Fréquence d'arrosage en été (jours)", required=True, default=7)
    watering_frequency_winter = fields.Integer(string="Fréquence d'arrosage en hiver (jours)", required=True, default=10)

    #---------------------------------RELATIONNAL FIELDS---------------------------------#
    plant_ids = fields.One2many('plantbased_plant', 'species_id', string="Plantes")