from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Order(models.Model):
    _name = 'trufflesapp.order'
    _description = 'The order of a Client'

    references=fields.Integer(string="References", required=True, default=lambda self: self.setReferences()) #ID Autoincrementable
    dateOrder=fields.Datetime(string="Date",help="The date of the order", required=True, default=fields.Datetime.now)
    base=fields.Float(string="Base", help="The total price of the orders without IVA", compute="setPriceBase", store=True)
    iva=fields.Selection(string="IVA", selection=[('zero','0%'), ('ten','10%'), ('twenty-one','21%')], default="zero")
    totalIva=fields.Float(string="TotalIVA", help="The total price of the order with IVA", compute="computeTotalIVA",store=True)
    state=fields.Selection(string="State", selection=[('D', 'Draft'), ('C', 'Confirmed'), ('I', 'Invoiced')], default="D")
    lines=fields.One2many("trufflesapp.orderlines", "orderid")
    vendor=fields.Many2one("res.partner", string="Vendor", required=True) #Relacion a modelo customers
    active=fields.Boolean(string="Is active",default=True)
    invoice=fields.Many2one("trufflesapp.invoice", string="Invoice")

    def setReferences(self):
        result = self.env['trufflesapp.order'].search_read()
        if len(result) == 0:
            return 1
        else:
           return result[-1]["references"] +1
        
    def checkStock(self):
        if self.lines== None:
            raise ValidationError("The order does not contain any products")
        else:
            for product in self.lines:
                weight = product.weight
                stockProducte = product.productid.stock
                total = stockProducte - weight
                if total < 0:
                    raise ValidationError("The stock for the products is insufficient")
                else:
                    product.productid.stock = total

    def desactivateOrders(self):
        orders = self.search([('state','in','(C, I)')])
        for order in orders:
            order.active = False

    @api.depends("lines")
    def setPriceBase(self):
        self.base = 0.0
        newPrice = 0.0
        for line in self.lines:
            newPrice = newPrice + line.totalprice
        self.base = newPrice

    @api.depends("iva", "base")
    def computeTotalIVA(self):
        for record in self:
            if record.iva == 'ten':
                record.totalIva = record.base + (record.base * 0.10)
            elif record.iva == 'twenty-one':
                record.totalIva = record.base + (record.base * 0.21)
            elif record.iva == 'zero':
                record.totalIva = record.base

    def confirmOrder(self):
        self.sudo().checkStock()
        self.state = 'C'

    def invoiceOrder(self):
        self.createInvoice()
        self.state = 'I'

    def createInvoice(self):
        infoInvoice = {
            "customer": self.vendor.id,
        }
        invoice = self.env["trufflesapp.invoice"].sudo().create(infoInvoice)
        for linesInvoice in self.lines:
            product = linesInvoice.productid
            units = linesInvoice.units
            linea = {
                "invoiceid": invoice.id,
                "productid": product.id,
                "units": units
            }
            self.env["trufflesapp.lines"].sudo().create(linea)
        self.invoice = invoice


        