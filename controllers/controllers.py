# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import json
from odoo.http import request, Response

class Trufflesapp(http.Controller):

    #
    #Product
    #

    #get
    @http.route(['/trufflesapp/getProduct', '/trufflesapp/getProduct/<int:productid>'], auth='public', type="http")
    def getProduct(self,productid=None, **kw):
        try:
            if productid:
                domain=[("id","=",productid)]
            else:
                domain=[]                                                                                        
            productInfo = http.request.env["trufflesapp.product"].sudo().search_read(domain,["name", "description", "category", "quality", "weight", "mesure", "price", "stock", "fullPath"])
            if not productInfo:
                data = json.dumps({'status': 400, 'message': 'Product not found'})
                return Response(data, content_type='application/json', status=400)
            result = {"status": 200, "result":productInfo}
            return http.Response(json.dumps(result).encode("utf8"),mimetype="application/json")
        except Exception as error:
            data={
                "status":404,
                "error":error
            }
            return data
    
    #
    #Category
    #

    #get
    @http.route(['/trufflesapp/getCategory/','/trufflesapp/getCategory/<int:categoryid>'], auth='public', type="http")
    def getCategory(self, categoryid=None, **kw):
        try:
            if categoryid:
                domain=[("id","=",categoryid)]
            else:
                domain=[]                                       
            categoryInfo = http.request.env["trufflesapp.category"].sudo().search_read(domain,["name", "description", "father", "children", "products"])
            if not categoryInfo:
                data = json.dumps({'status': 400, 'message': 'Category not found'})
                return Response(data, content_type='application/json', status=400)
            result = {"status": 200, "result":categoryInfo}
            return http.Response(json.dumps(result).encode("utf8"),mimetype="application/json")
        except Exception as error:
            data={
                "status":404,
                "error":error
            }
            return data
    
    #
    #Order
    #
        
    #get
    @http.route(['/trufflesapp/getOrder/','/trufflesapp/getOrder/<int:orderid>'], auth='public', type="http")
    def getOrder(self, orderid=None, **kw):
        try:
            if orderid:
                domain=[("id","=",orderid)]
            else:
                domain=[]                                                                                                                            
            orderInfo = http.request.env["trufflesapp.order"].sudo().search_read(domain,["name", "base", "iva", "totalIva", "state", "vendor", "lines", "invoice"])
            if not orderInfo:
                data = json.dumps({'status': 400, 'message': 'Order not found'})
                return Response(data, content_type='application/json', status=400)
            
            result = {"status": 200, "result":orderInfo}
            return http.Response(json.dumps(result).encode("utf8"),mimetype="application/json")
        except Exception as error:
            data={
                "status":404,
                "error":error
            }
            return data 
    #añadir
    @http.route('/trufflesapp/addOrder', type='json', auth='public', methods=['POST'], csrf=False)
    def addOrder(self, **kw):
        response = request.httprequest.json
        try:
            vendorid = response.get('vendor')
            if not vendorid:
                return {"status": 400, "error": "Vendor is required."}
                
            base = response.get('base')
            if base:
                return {"status": 400, "error": "You cant change the price"}
            
            totalIva = response.get('totalIva')
            if totalIva:
                return {"status": 400, "error": "You cant change the price"}
            
            active = response.get('active')
            if active:
                return {"status": 400, "error": "You dont have permissions to modify the active"}
            
            invoice = response.get('invoice')
            if invoice:
                return {"status": 400, "error": "You dont have permissions to modify the invoice"}
            
            partner = request.env['res.partner'].sudo().browse(vendorid)
            if not partner.exists():
                return {"status": 404, "error": "Vendor not found."}

            if response.get('state') == 'Confirmed':
                result.confirmOrder()

            result = http.request.env["trufflesapp.order"].sudo().create(response)
            data={
                "status":201,
                "id":result.id
            }
            return data
        except Exception as error:
            data={
                "status":404,
                "error":error
            }
            return data

    
    #borrar
    @http.route('/trufflesapp/deleteOrder/<int:orderid>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def deleteOrder(self, orderid):
        order = request.env['trufflesapp.order'].sudo().browse(orderid)
        try:
            if not order.exists():
                data = json.dumps({'status': 400, 'message': 'Order not found'})
                return Response(data, content_type='application/json', status=400)

            order.unlink()

            data = json.dumps({'status': 200, 'message': 'Order deleted successfully'})
            return Response(data, content_type='application/json', status=200)
    
        except Exception as error:
            data = json.dumps({'status': 404, 'message': error})
            return Response(data, content_type='application/json', status=400)

    #actualizar
    @http.route('/trufflesapp/updateOrder', type='json', auth='public', methods=['PUT'])
    def updateOrder(self, **kw):
       response = request.httprequest.json
       try:
            result = http.request.env["trufflesapp.order"].sudo().search([("id","=",response["id"])])
            if not result.exists():
                data={
                "status":400,
                "id":result.id
                }   
                return data
            
            base = response.get('base')
            if base:
                return {"status": 400, "error": "You cant change the price"}
            
            totalIva = response.get('totalIva')
            if totalIva:
                return {"status": 400, "error": "You cant change the price"}
            
            active = response.get('active')
            if active:
                return {"status": 400, "error": "You dont have permissions to modify the active"}
            
            invoice = response.get('invoice')
            if invoice:
                return {"status": 400, "error": "You dont have permissions to modify the invoice"}

            if response.get('state') not in ['Draft', 'Confirmed']:
                data={
                    "status":400,
                    "error":"Invalid state value. State must be Draft or Confirmed"
                    }   
                return data
            
            if response.get('state') == 'Confirmed':
                result.confirmOrder()

            result.sudo().write(response)
            data={
                "status":200,
                "id":result.id
            }
            return data
       except Exception as error:
            data={
                "status":404,
                "error":error
            }
            return data
       
    #   
    #OrderLine
    #
        
    #get
    @http.route(['/trufflesapp/getOrderLine/','/trufflesapp/getOrderLine/<int:orderlineid>'], auth='public', type="http")
    def getOrderLine(self, orderlineid=None, **kw):
        if orderlineid:
            domain=[("id","=",orderlineid)]
        else:
            domain=[]
        orderLineInfo = http.request.env["trufflesapp.orderlines"].sudo().search_read(domain,["productid", "units", "mesure", "weight", "totalprice", "orderid"])
        if not orderLineInfo:
            data = json.dumps({'status': 400, 'message': 'Order Line not found'})
            return Response(data, content_type='application/json', status=400)
        result = {"status": 200, "result":orderLineInfo}
        return http.Response(json.dumps(result).encode("utf8"),mimetype="application/json")
         
    #añadir
    @http.route('/trufflesapp/addOrderLine', type='json', auth='public', methods=['POST'], csrf=False)
    def addOrderLine(self, **kw):
        response = request.httprequest.json
        try:

            productid = response.get('productid')
            if not productid:
                return {"status": 400, "error": "Is necessary to specify the product id"}
            
            product = request.env['trufflesapp.product'].sudo().browse(productid)
            if not product.exists():
                return {'status': 400, 'message': 'Product not found'}

            mesure = response.get('mesure')
            if not mesure:
                return {"status": 400, "error": "Is necessary to specify the type of mesure"}
            
            orderid = response.get('orderid')
            if not orderid:
                return {"status": 400, "error": "Is necessary to specify the order id"}
            
            order = request.env['trufflesapp.order'].sudo().browse(orderid)
            if not order.exists():
                return {'status': 400, 'message': 'Order not found'}

            result = http.request.env["trufflesapp.orderlines"].sudo().create(response)
            data={
                "status":201,
                "id":result.id
            }
            return data
        except Exception as error:
            data={
                "status":404,
                "error":error
            }
            return data

    #borrar
    @http.route('/trufflesapp/deleteOrderLine/<int:lineid>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def deleteOrderLine(self, lineid):

        line = request.env['trufflesapp.orderlines'].sudo().browse(lineid)
        try:
            if not line.exists():
                data = json.dumps({'status': 400, 'message': 'Order Line not found'})
                return Response(data, content_type='application/json', status=400)

            line.unlink()

            data = json.dumps({'status': 200, 'message': 'Order Line deleted successfully'})
            return Response(data, content_type='application/json', status=200)
    
        except Exception as error:
            data = json.dumps({'status': 404, 'message': error})
            return Response(data, content_type='application/json', status=400)

    #actualizar
    @http.route('/trufflesapp/updateOrderLine', type='json', auth='public', methods=['PUT'])
    def updateOrderLine(self, **kw):
       response = request.httprequest.json
       try:
            result = http.request.env["trufflesapp.orderlines"].sudo().search([("id","=",response["id"])])
            if not result.exists():
                data={
                "status":400,
                "id":result.id
                }   
                return data
            
            if response.get('weight'):
                data={
                "status":400,
                "error":"Yo cant change the weight"
                }
                return data
            
            if response.get('totalprice'):
                data={
                "status":400,
                "error":"Yo cant change the total price"
                }
                return data

            result.sudo().write(response)
            data={
                "status":201,
                "id":result.id
            }
            return data
       except Exception as error:
            data={
                "status":404,
                "error":error
            }
            return data
       
    #   
    #Weight
    #
        
    #get
    @http.route(['/trufflesapp/getWeight/','/trufflesapp/getWeight/<int:weightid>'], auth='public', type="http")
    def getWeight(self, weightid=None, **kw):
        if weightid:
            domain=[("id","=",weightid)]
        else:
            domain=[]
        weightInfo = http.request.env["trufflesapp.weight"].sudo().search_read(domain,["name", "type", "mesure"])
        if not weightInfo:
            data = json.dumps({'status': 400, 'message': 'Weight not found'})
            return Response(data, content_type='application/json', status=400)
        result = {"status": 200, "result":weightInfo}
        return http.Response(json.dumps(result).encode("utf8"),mimetype="application/json")
    
    #   
    #Quality
    #
        
    #get
    @http.route(['/trufflesapp/getQuality/','/trufflesapp/getQuality/<int:qualityid>'], auth='public', type="http")
    def getQuality(self, qualityid=None, **kw):
        if qualityid:
            domain=[("id","=",qualityid)]
        else:
            domain=[]
        qualityInfo = http.request.env["trufflesapp.quality"].sudo().search_read(domain,["name", "description"])
        if not qualityInfo:
            data = json.dumps({'status': 400, 'message': 'Quality not found'})
            return Response(data, content_type='application/json', status=400)
        result = {"status": 200, "result":qualityInfo}
        return http.Response(json.dumps(result).encode("utf8"),mimetype="application/json")
    
    #   
    #Invoice
    #

    #get
    @http.route(['/trufflesapp/getInvoice/<int:partner_id>'], auth='public', type="http")
    def getInvoice(self, partner_id=None, **kw):
        if partner_id:
            partner = request.env['res.partner'].sudo().browse(partner_id)
            if not partner.exists():
                result = {"status": 400, "result":"Customer not found"}
                return http.Response(json.dumps(result).encode("utf8"),mimetype="application/json")

            invoices = request.env["trufflesapp.invoice"].sudo().search([('customer', '=', partner_id)])
            if not invoices:
                result = {"status": 400, "result":"No invoices found for this customer"}
                return http.Response(json.dumps(result).encode("utf8"),mimetype="application/json")

            invoice_data = invoices.read(["name", "description", "base", "iva", "totalIva", "state", "customer"])
            result = {"status": 200, "result": invoice_data}
            return http.Response(json.dumps(result).encode("utf8"),mimetype="application/json")
        else:
            result = {"status": 400, "message": "It is necessary to enter a partner id"}
            return Response(json.dumps(result), content_type='application/json', status=400)
    
    '''
    #añadir
        
    #Confirmar
    @http.route('/trufflesapp/confirmOrder', type='json', auth='public', methods=['POST'], csrf=False)
    def confirmOrder(self, orderid):
        order = request.env['trufflesapp.order'].sudo().browse(orderid)
        if order:
            try:
                order.confirmOrder()
                data={
                    "status":201,
                    "message":'Order confirmed'
                }
                return data
            except Exception as error:
                data={
                    "status":400,
                    "error":error
                }
                return data
        else:
            data={
                    "status":404,
                    "error":"Order not found"
                }
            return data

    #Invoiced
    @http.route('/trufflesapp/invoiceOrder', type='json', auth='public', methods=['POST'], csrf=False)
    def invoiceOrder(self, orderid):
        order = request.env['trufflesapp.order'].sudo().browse(orderid)
        if order:
            try:
                order.invoiceOrder()
                data={
                    "status":201,
                    "message":'Order confirmed'
                }
                return data
            except Exception as error:
                data={
                    "status":400,
                    "error":error
                }
                return data
        else:
            data={
                    "status":404,
                    "error":"Order not found"
                }
            return data


    '''