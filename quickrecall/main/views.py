# views.py

from django.http import HttpResponse

from quickrecall.main.models import Visitor

def main(request):
    visitor = Visitor()
    visitor.ip = request.META["REMOTE_ADDR"]
    visitor.put()

    result = ""
    visitors = Visitor.all()
    visitors.order("-added_on")

    for visitor in visitors.fetch(limit=40):
        result += visitor.ip + u" visited on " + unicode(visitor.added_on) + u""

    return HttpResponse(result)

