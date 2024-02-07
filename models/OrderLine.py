from odoo import models, fields, api

class Orderlines(models.Model):
    _name = 'trufflesapp.orderlines'
    _description = 'The Order Lines'

    productid=fields.Many2one("trufflesapp.product", string="Product", required=True)
    units=fields.Float(string="Units", default=1, required=True)
    mesure=fields.Char(string="Mesure", required=True, compute='getMesure')
    weight=fields.Float(string="Total Weigth", compute="getTotalWeight", required=True) #Peso
    totalprice=fields.Float(string="Total Price", help="The total Price", compute="computeTotalPrice", required=True)
    priceProduct=fields.Float(string="Product Price", help="Price of the product", compute="getPrice", required=True)
    weightProduct=fields.Float(string="Product Weight", compute="getWeightProducts", help="Weight of the product") #Peso
    orderid=fields.Many2one("trufflesapp.order", string="Order")

    @api.depends("productid")
    def getMesure(self):
        for record in self:
            record.mesure = record.productid.weight.mesure

    @api.depends("productid")
    def getPrice(self):
        for record in self:
            record.priceProduct = record.productid.price

    @api.depends("productid")
    def getWeightProducts(self):
        for record in self:
            record.weightProduct = record.productid.weight.name

    @api.depends("units", "priceProduct")
    def computeTotalPrice(self):
        for record in self:
            record.totalprice = record.units * record.priceProduct

    @api.depends("units", "productid")
    def getTotalWeight(self):
        for record in self:
            record.weight = record.units * record.weightProduct


