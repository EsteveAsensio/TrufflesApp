from odoo import models, fields, api


class Product(models.Model):
    _name = 'trufflesapp.product'
    _description = 'The product with related information'

    name=fields.Char(string="Name", help="Name of the category", required=True)
    description=fields.Html(string="Description", help="Description of the weight")
    category=fields.Many2one("trufflesapp.category", string="Category", required=True)
    quality=fields.Many2one("trufflesapp.quality", string="Quality")
    weight=fields.Many2one("trufflesapp.weight", string="Weight", required=True)
    price=fields.Float(string="Price", help="Price of the product", required=True)
    stock=fields.Float(string="Stock", help="Stock of the product", required=True)
    photo = fields.Binary(string="Photo", help="A photo of the product", store=True)
    lines=fields.One2many("trufflesapp.lines", "productid") #Modeo lineas
    #invoice=fields.Many2one("trufflesapp.invoice", string="Invoice")

