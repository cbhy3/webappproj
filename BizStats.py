from openpyxl.workbook import Workbook
from tempfile import NamedTemporaryFile
from flask import send_file, redirect, url_for
from datetime import datetime, timedelta

import Order, shelve, Product, openpyxl

def GetStats():
    LifetimeSales = 0
    MonthlySales = 0
    TopSelling = {}
    Sold = {}
    weight = 0
    with shelve.open('Orders') as OrdersDB:
        for i in OrdersDB:
            order = OrdersDB[i]
            if order.status != "PaymentProcessing":
                LifetimeSales += float(order.subtotal)      #Lifetime Sales calculation
        for i in OrdersDB:
            order = OrdersDB[i]
            if datetime.strptime(order.date, "%d/%m/%Y") - datetime.today() < timedelta(days=31) and order.status != "PaymentProcessing":
                MonthlySales += float(order.subtotal)          #Monthly Sales calculation

        for i in OrdersDB:
            order = OrdersDB[i]
            for x in order.Products:
                if order.status != "PaymentProcessing":
                    TopSelling.setdefault(order.Products[x][1].name, 0)
                    TopSelling[order.Products[x][1].name] += order.Products[x][0]
        temp = dict(sorted(TopSelling.items(), key=lambda item: item[1], reverse=True))       #Top Selling Calculation
        RealTopSelling = dict(list(temp.items())[:10]) #Keep only top 10 selling products

        for i in OrdersDB:
            for x in OrdersDB[i].Products:
                weight += OrdersDB[i].Products[x][1].weight * OrdersDB[i].Products[x][0]
        Co2 = (weight/1000) * 4.5
        Water = (weight/1000) * 1500
    return {"LifetimeSales": LifetimeSales,
            "MonthlySales": MonthlySales,
            "TopSelling": RealTopSelling,
            "Co2": Co2,
            "Water": Water}

def exportXL():
    wb = Workbook()
    ws = wb.active
    ws.append(["OrderID","OrderSubtotal","OrderReferenceNum","DeliveryAddress","OrderDate","OrderedBy", "VoucherUsed", "Products+Quantity"])
    with shelve.open('Orders') as OrdersDB:
        orders = list(OrdersDB.values())

        for order in orders:
            products = []
            for product in order.Products:
                products.append((order.Products[product][1].name, order.Products[product][0]))
            a = str(products)
            ws.append([order.id, order.subtotal, order.payment_method, order.address, order.date, order.user, order.voucher, a ])
    with NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        temp_file_name = tmp.name  # Get the temp file name
        wb.save(temp_file_name)
    return send_file(temp_file_name, as_attachment=True, download_name="Orders.xlsx",mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')




