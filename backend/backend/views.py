import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from model.predict import predict

@csrf_exempt  # Disables CSRF protection for this view. Be cautious about doing this in production.
@require_http_methods(["POST"])  # Allows only POST requests.
def handlePredict(request):
    # Get the POST data from request.
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON."}, status=400)

    if 'strokes' not in data:
        return JsonResponse({"error": "No strokes provided."}, status=400)

    strokes = data['strokes']
    prediction, prob = predict(strokes, "../model/tut2-model.pt", "../model/classes.csv")
    
    # Process the data (this is just an example; you should replace it with your logic).
    response_data = {"prediction": prediction, "probability": prob}

    # Return a JSON response.
    return JsonResponse(response_data, status=200)