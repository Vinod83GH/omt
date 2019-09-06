from django.http import JsonResponse
from .tasks import process_input_file
def names(request):
    return JsonResponse({'names': ['William', 'Rod', 'Grant']})

def import_data(request):
    # Write your data import logic below
    process_input_file()
    return JsonResponse({'message':'Successfully imported data'})


