# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import json

class Trufflesapp(http.Controller):
    @http.route(['/trufflesapp/getProduct', '/trufflesapp/getProduct/<int:productid>'], auth='public', type="http")
    def getProduct(self,productid=None, **kw):
        if productid:
            domain=[("id","=",productid)]
        else:
            domain=[]
        productInfo = http.request.env["trufflesapp.product"].sudo().search_read(domain,["name", "description", "category"])
        result = {"status": 200, "result":productInfo}
        return http.Response(json.dumps(result).encode("utf8"),mimetype="application/json")

    @http.route(['/trufflesapp/getCategory/','/trufflesapp/getCategory/<int:categoryid>'], auth='public', type="http")
    def getCategory(self, categoryid=None, **kw):
        if categoryid:
            domain=[("id","=",categoryid)]
        else:
            domain=[]
        categoryInfo = http.request.env["trufflesapp.category"].sudo().search_read(domain,["name", "description"])
        result = {"status": 200, "result":categoryInfo}
        return http.Response(json.dumps(result).encode("utf8"),mimetype="application/json")

    @http.route(['/trufflesapp/getOrder/','/trufflesapp/getOrder/<int:orderid>'], auth='public', type="http")
    def getOrder(self, orderid=None, **kw):
        if orderid:
            domain=[("id","=",orderid)]
        else:
            domain=[]
        orderInfo = http.request.env["trufflesapp.order"].sudo().search_read(domain,["name"])
        result = {"status": 200, "result":orderInfo}
        return http.Response(json.dumps(result).encode("utf8"),mimetype="application/json")
