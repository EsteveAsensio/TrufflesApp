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
        if productid:
            domain=[("id","=",productid)]
        else:
            domain=[]
        productInfo = http.request.env["trufflesapp.product"].sudo().search_read(domain,["name", "description", "category"])
        result = {"status": 200, "result":productInfo}
        return http.Response(json.dumps(result).encode("utf8"),mimetype="application/json")

    #añadir
    @http.route('/trufflesapp/addProduct', type='http', auth='public', methods=['POST'], csrf=False)
    def addCategory(self, **kw):
        try:
            data = json.loads(request.httprequest.data.decode('utf-8'))
        except json.JSONDecodeError:
            response_data = json.dumps({'status': 400, 'message': '¡Incorrect JSON!'})
            return Response(response_data, content_type='application/json', status=400)
        
        if 'name' not in data or not data['name']:
            response_data = json.dumps({'status': 400, 'message': 'The name field must be filled in.'})
            return Response(response_data, content_type='application/json', status=400)
        
        model = request.env['trufflesapp.product'].sudo()
        product = model.create({
            'name': data.get('name'),
            'description': data.get('description', ''),
            'father': data.get('father', False)
        })

    #actualizar
    @http.route('/trufflesapp/updateProduct/<int:productid>', type='http', auth='public', methods=['POST'], csrf=False)
    def updateCategory(self, productid, **kw):
        try:
            data = json.loads(request.httprequest.data.decode('utf-8'))
        except json.JSONDecodeError:
            response_data = json.dumps({'status': 400, 'message': '¡Incorrect JSON!'})
            return Response(response_data, content_type='application/json', status=400)
        
        model = request.env['trufflesapp.product'].sudo()
        product = model.browse([productid])

        if not product.exists():
            response_data = json.dumps({'status': 400, 'message': 'Product not found.'})
            return Response(response_data, content_type='application/json', status=400)

        product.write({
            'name': data.get('name', product.name),
            'description': data.get('description', product.description),
            'father': data.get('father', product.father.id if product.father else False)
        })

        response_data = json.dumps({'status': 200, 'message': 'Product successfully modified.'})
        return Response(response_data, content_type='application/json', status=200)
    
    #borrar
    @http.route('/trufflesapp/deleteProduct/<int:productid>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def deleteCategory(self, productid):
        model = request.env['trufflesapp.product'].sudo()
        product = model.browse([productid])

        if not product.exists():
            response_data = json.dumps({'status': 400, 'message': 'Product not found'})
            return Response(response_data, content_type='application/json', status=400)

        product.unlink()

        response_data = json.dumps({'status': 200, 'message': 'Product successfully eliminated.'})
        return Response(response_data, content_type='application/json', status=200)
    
    #
    #Category
    #

    #get
    @http.route(['/trufflesapp/getCategory/','/trufflesapp/getCategory/<int:categoryid>'], auth='public', type="http")
    def getCategory(self, categoryid=None, **kw):
        if categoryid:
            domain=[("id","=",categoryid)]
        else:
            domain=[]
        categoryInfo = http.request.env["trufflesapp.category"].sudo().search_read(domain,["name", "description"])
        result = {"status": 200, "result":categoryInfo}
        return http.Response(json.dumps(result).encode("utf8"),mimetype="application/json")

    #añadir
    @http.route('/trufflesapp/addCategory', type='http', auth='public', methods=['POST'], csrf=False)
    def addCategory(self, **kw):
        try:
            data = json.loads(request.httprequest.data.decode('utf-8'))
        except json.JSONDecodeError:
            response_data = json.dumps({'status': 400, 'message': '¡Incorrect JSON!'})
            return Response(response_data, content_type='application/json', status=400)
        
        if 'name' not in data or not data['name']:
            response_data = json.dumps({'status': 400, 'message': 'The name field must be filled in.'})
            return Response(response_data, content_type='application/json', status=400)
        
        model = request.env['trufflesapp.category'].sudo()
        category = model.create({
            'name': data.get('name'),
            'description': data.get('description', ''),
            'father': data.get('father', False)
        })

        response_data = json.dumps({'status': 200, 'category_id': category.id, 'message': 'Category successfully established.'})
        return Response(response_data, content_type='application/json', status=200)
    
    #actualizar
    @http.route('/trufflesapp/updateCategory/<int:categoryid>', type='http', auth='public', methods=['POST'], csrf=False)
    def updateCategory(self, categoryid, **kw):
        try:
            data = json.loads(request.httprequest.data.decode('utf-8'))
        except json.JSONDecodeError:
            response_data = json.dumps({'status': 400, 'message': '¡Incorrect JSON!'})
            return Response(response_data, content_type='application/json', status=400)
        
        model = request.env['trufflesapp.category'].sudo()
        category = model.browse([categoryid])

        if not category.exists():
            response_data = json.dumps({'status': 400, 'message': 'Category not found.'})
            return Response(response_data, content_type='application/json', status=400)

        category.write({
            'name': data.get('name', category.name),
            'description': data.get('description', category.description),
            'father': data.get('father', category.father.id if category.father else False)
        })

        response_data = json.dumps({'status': 200, 'message': 'Category successfully modified.'})
        return Response(response_data, content_type='application/json', status=200)
    
    #borrar
    @http.route('/trufflesapp/deleteCategory/<int:categoryid>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def deleteCategory(self, categoryid):
        model = request.env['trufflesapp.category'].sudo()
        category = model.browse([categoryid])

        if not category.exists():
            response_data = json.dumps({'status': 400, 'message': 'Category not found'})
            return Response(response_data, content_type='application/json', status=400)

        category.unlink()

        response_data = json.dumps({'status': 200, 'message': 'Category successfully eliminated.'})
        return Response(response_data, content_type='application/json', status=200)
    
    #
    #Order
    #

    #get
    @http.route(['/trufflesapp/getOrder/','/trufflesapp/getOrder/<int:orderid>'], auth='public', type="http")
    def getOrder(self, orderid=None, **kw):
        if orderid:
            domain=[("id","=",orderid)]
        else:
            domain=[]
        orderInfo = http.request.env["trufflesapp.order"].sudo().search_read(domain,["name"])
        result = {"status": 200, "result":orderInfo}
        return http.Response(json.dumps(result).encode("utf8"),mimetype="application/json")
