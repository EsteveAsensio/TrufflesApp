from odoo import models, fields, api


class Invoice(models.Model):
    _name = 'trufflesapp.invoice'
    _description = 'The invoice about the products'

    references=fields.Integer(string="References", required=True, default=lambda self: self.setReferences()) #ID Autoincrementable
    description=fields.Html(string="Description", help="Description of the Invoice")
    dateInvoice=fields.Datetime(string="Date",help="The date of the invoice", required=True, default=fields.Datetime.now)
    base=fields.Float(string="Base", help="The total price of the invoice without IVA", compute="setPriceBase", required=True)
    iva=fields.Selection(string="IVA", selection=[('zero','0%'), ('ten','10%'), ('twenty-one','21%')], default="zero")
    totalIva=fields.Float(string="TotalIVA", help="The total price of the invoice with IVA", compute="computeTotalIVA")
    state=fields.Selection(string="State", selection=[('D', 'Draft'), ('C', 'Confirmed')], default="D")
    lines=fields.One2many("trufflesapp.lines", "invoiceid") #linea (nuevo modelo)
    customer=fields.Char(string="Customer") #Relacion a modelo customers
    
    def init(self):
        self.setPriceBase()

    def setReferences(self):
        result = self.env['trufflesapp.invoice'].search_read()
        if len(result) == 0:
            return 1
        else:
           return result[-1]["references"] +1
        
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

    def confirmInvoice(self):
        self.state = 'C'