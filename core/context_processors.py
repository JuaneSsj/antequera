from .models import BusinessProfile

def business_profile(request):
    """
    Makes the business profile available to all templates.
    """
    obj, created = BusinessProfile.objects.get_or_create(defaults={
        'description': "Bienvenido a Training Home, donde tu progreso es nuestra prioridad."
    })
    return {'business_profile': obj}
