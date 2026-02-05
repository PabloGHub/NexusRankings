# python
# Archivo: `ranqueo/views.py`
import json
from django.db import transaction
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

from .models import Game, Mod, Ranking  # ajustar nombres de modelos según tu app

@require_POST
def update_ranking(request, game_id):
    try:
        pld = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return HttpResponseBadRequest('JSON inválido')

    if not isinstance(pld, list):
        return HttpResponseBadRequest('Se esperaba una lista de objetos')

    game = get_object_or_404(Game, pk=game_id)

    seen_positions = set()
    new_rankings = []

    for idx, item in enumerate(pld):
        if not isinstance(item, dict) or 'position' not in item or 'mod_id' not in item:
            return HttpResponseBadRequest(f'Entrada inválida en índice {idx}')

        try:
            position = int(item['position'])
        except (ValueError, TypeError):
            return HttpResponseBadRequest(f'Position inválida en índice {idx}')

        mod_id = item['mod_id']

        if position in seen_positions:
            return HttpResponseBadRequest(f'Posición duplicada: {position}')
        seen_positions.add(position)

        # Intentar buscar el Mod por campo razonable (ajusta según tu modelo)
        mod = None
        try:
            mod = Mod.objects.get(pk=mod_id)
        except Exception:
            try:
                mod = Mod.objects.get(mod_id=mod_id)
            except Exception:
                return HttpResponseBadRequest(f'Mod no encontrado: {mod_id}')

        new_rankings.append(Ranking(game=game, mod=mod, position=position))

    # Guardar en bloque dentro de una transacción: limpiamos y creamos
    with transaction.atomic():
        Ranking.objects.filter(game=game).delete()
        Ranking.objects.bulk_create(new_rankings)

    return JsonResponse({'status': 'ok', 'saved': len(new_rankings)})
