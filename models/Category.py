from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Category(models.Model):
    _name = 'trufflesapp.category'
    _description = 'Add the category of each product or another category'

    name=fields.Char(string="Name", help="Name of the category", required=True)
    description=fields.Html(string="Description", help="Description of the Weigth")
    father=fields.Many2one("trufflesapp.category", string="CategoryFather")
    children=fields.One2many("trufflesapp.category", "father")
    products=fields.One2many("trufflesapp.product", "category")
