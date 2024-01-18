from odoo import models, fields, api
from odoo.exceptions import Warning

class Lines(models.Model):
    _name = 'trufflesapp.lines'
    _description = 'The Invoice Lines'

    productid=fields.Many2one("trufflesapp.product", string="Product", required=True)
    weight=fields.Float(string="Quantity", required=True) #Peso
    totalprice=fields.Float(string="Total Price", help="The total Price", required=True)
    priceProduct=fields.Float(string="Price", help="Price of the product", required=True)
    weightProduct=fields.Float(string="Prodct Weight", help="Weight of the product") #Peso
    invoiceid=fields.Many2one("trufflesapp.invoice", string="Invoice")

    @api.onchange("productid")
    def getPrice(self):
        self.priceProduct = self.productid.price

    @api.onchange("productid")
    def getWeightProducts(self):
        self.weightProduct = self.productid.weight.name

    @api.onchange("weight")
    def computeTotalPrice(self):
        if self.weightProduct > 0:
            self.totalprice = (self.weight / self.weightProduct) * self.priceProduct
        else:
            self.totalprice = 0.0

