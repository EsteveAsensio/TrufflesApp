from odoo import models, fields, api

class Weight(models.Model):
    _name = 'trufflesapp.weight'
    _description = 'Control the weight of the Truffles'

    name=fields.Float(string="Quantity", help="Amount of weight", required=True)
    type=fields.Char(string="Type", help="Type of the weight/packages") #ex: Granel
    description=fields.Html(string="Description", help="Description of the weight")
    product=fields.One2many("trufflesapp.product", "weight")


