from django.http import JsonResponse
def names(request):
    return JsonResponse({'names': ['William', 'Rod', 'Grant']})

def import_data(request):
    # Write your data import logic below
    return JsonResponse({'names-1': ['William-1', 'Rod-1', 'Grant-1']})