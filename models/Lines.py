from odoo import models, fields, api
from odoo.exceptions import Warning

class Lines(models.Model):
    _name = 'trufflesapp.lines'
    _description = 'The Invoice Lines'

    productid=fields.Many2one("trufflesapp.product", string="Product", required=True)
    weight=fields.Float(string="Quantity", required=True) #Peso
    totalprice=fields.Float(string="Total Price", help="The total Price", compute="computeTotalPrice", required=True)
    priceProduct=fields.Float(string="Product Price", help="Price of the product", compute="getPrice", required=True)
    weightProduct=fields.Float(string="Product Weight", compute="getWeightProducts", help="Weight of the product") #Peso
    invoiceid=fields.Many2one("trufflesapp.invoice", string="Invoice")

    @api.depends("productid")
    def getPrice(self):
        for record in self:
            record.priceProduct = record.productid.price

    @api.depends("productid")
    def getWeightProducts(self):
        for record in self:
            record.weightProduct = record.productid.weight.name

    @api.depends("weight", "weightProduct", "priceProduct")
    def computeTotalPrice(self):
        for record in self:
            if record.weightProduct > 0:
                record.totalprice = (record.weight / record.weightProduct) * record.priceProduct
            else:
                record.totalprice = 0.0

