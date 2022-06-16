from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render
from .models import Order
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
from weasyprint import HTML, CSS

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, pk = order_id)
    total = 0
    for i in order.orderdetail_set.all():
        total += i.price * i.qty
    return render(request, "admin/factory/order/detail.html", {"order" : order, "total" : total})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    total = 0
    for i in order.orderdetail_set.all():
        total += i.price * i.qty
    html = render_to_string("factory/order/pdf.html", {"order" : order, "total" : total})
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"filename=order_{order_id}.pdf"
    weasyprint.HTML(string=html).write_pdf(response)

    return response