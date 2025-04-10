from odoo import models, fields, api
from datetime import datetime, timedelta

class Plant(models.Model):
    
    #---------------------------------DESCRIPTION---------------------------------#
    _name = "plantbased_plant"
    _description = "Vos plantes"
    _order = "name desc"

    #---------------------------------BASIC FIELDS---------------------------------#
    name = fields.Char(string="Nom", required=True)
    photo = fields.Image()
    

    #---------------------------------RELATIONNAL FIELDS---------------------------------#
    species_id = fields.Many2one('plantbased_plant_species', string="Espèce", required=True)
    room_id = fields.Many2one('plantbased_plant_room', string="Pièce", required=True)
    watering_ids = fields.One2many('plantbased_plant_watering', 'plant_id', string="Historique des arrosages")

    #---------------------------------COMPUTED---------------------------------#
    last_watering_date = fields.Date(string="Dernier arrosage", compute="_compute_last_watering_date", store=True)
    plant_health = fields.Selection([
        ('healthy', 'En bonne santé'),
        ('not_that_healthy', 'Bof bof la santé'),
        ('not_healthy', '"En train de die')
    ], string="État de la plante", compute="_compute_last_watering_health", store=True)
    water_need_status = fields.Selection(
        selection=[
            ('ok', 'Ok'),
            ('thirsty', 'A soif'),
            ('dry', 'Asséchée')           
            
            
        ],
        string="Besoin en eau",
        compute="_compute_water_need_status",
        store=True
    )

     #---------------------------------COMPUTED METHODS---------------------------------#
    @api.depends('watering_ids.date')
    def _compute_last_watering_date(self):
        for plantbased_plant in self:
            last_watering = plantbased_plant.watering_ids.sorted(lambda w: w.date, reverse=True)[:1]
            plantbased_plant.last_watering_date = last_watering.date if last_watering else None

    @api.depends('watering_ids.plant_health')
    def _compute_last_watering_health(self):
        for plantbased_plant in self:
            last_watering = plantbased_plant.watering_ids.sorted(lambda w: w.date, reverse=True)[:1]
            plantbased_plant.plant_health = last_watering.plant_health

    @api.depends('last_watering_date', 'species_id.watering_frequency_summer', 'species_id.watering_frequency_winter')
    def _compute_water_need_status(self):
        """
        Calcul du statut "Besoin en eau" basé sur la dernière date d'arrosage,
        la fréquence d'arrosage définie dans la fiche espèce et la saison actuelle.
        """
        for plant in self:
            # Vérifier si une date d'arrosage est disponible
            if not plant.last_watering_date:
                plant.water_need_status = 'dry'  # Considérer comme "Asséchée" par défaut
                continue

            # Récupérer la date actuelle et s'assurer qu'elle est au format datetime.date
            today = fields.Date.today()

            # Vérifier que la date d'arrosage est également au format datetime.date
            last_watering_date = plant.last_watering_date.date() if isinstance(plant.last_watering_date, datetime) else plant.last_watering_date

            # Déterminer la saison actuelle
            is_summer = today.month in [3, 4, 5, 6, 7, 8]  # Printemps et été
            frequency = (plant.species_id.watering_frequency_summer if is_summer
                        else plant.species_id.watering_frequency_winter)

            # Calcul de la différence en jours entre aujourd'hui et le dernier arrosage
            days_since_watering = (today - last_watering_date).days

            # Déterminer le statut en fonction de la fréquence et de la différence
            if days_since_watering > frequency + 3:
                plant.water_need_status = 'dry'  # Asséchée
            elif days_since_watering > frequency:
                plant.water_need_status = 'thirsty'  # À soif
            else:
                plant.water_need_status = 'ok'  # Ok

    