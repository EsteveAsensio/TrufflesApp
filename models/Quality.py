from odoo import models, fields, api


class Quality(models.Model):
    _name = 'trufflesapp.quality'
    _description = 'Control the quality of the Truffles'

    name=fields.Char(string="Type", help="Type of the quality", required=True) #ex: Medium
    description=fields.Html(string="Description", help="Description of the quality")
    product=fields.One2many("trufflesapp.product", "quality")


