from django.http import HttpResponseRedirect


class DisneyMiddleware:

    def process_request(self, request):

        if 'disney' in request.GET:
            return HttpResponseRedirect("http://www.disney.com")

        return None