from odoo import models, fields

class Room(models.Model):

    #---------------------------------DESCRIPTION---------------------------------#
    _name = 'plantbased_plant_room'
    _description = 'Pièce où se trouve votre plante'

    #---------------------------------BASIC FIELDS---------------------------------#
    name = fields.Char(string="Nom", required=True)

    #---------------------------------RELATIONNAL FIELDS---------------------------------#
    plant_ids = fields.One2many('plantbased_plant', 'room_id', string="Plantes")