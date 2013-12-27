from django.conf import settings

def date_formats(request):
    return {
        'date_format_long': 'l j F Y',
    }
    
def serve_media_locally(request):
  return {'SERVE_MEDIA_LOCALLY': settings.SERVE_MEDIA_LOCALLY}
    