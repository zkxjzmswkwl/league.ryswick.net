from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from summoners.models import Summoner
from summoners.logic import service
from summoners.logic import selectors

@csrf_exempt
def insert_summoner(request):
    if request.method == "POST":
        payload = request.POST

        name = payload.get("name", None)
        tag_line = payload.get("tag_line", None)

        if name is None or tag_line is None:
            return HttpResponse("Error. TODO: actual error.")

        # Check if we already have this account indexed.
        query = selectors.select_by_riotid(name=name, tag_line=tag_line)
        already_tracked = query != None

        if not already_tracked:
            service.start_tracking(name=name, tag_line=tag_line)
            # response = service.get_puuid_by_riotid(name="EZREAL FISTER", tag_line="FISTD")
            # service.commit_summoner(
            #     puuid=response.get("puuid"),
            #     name=response.get("gameName"),
            #     tag_line=response.get("tagLine"))
            return HttpResponse("Started tracking")
        

        return HttpResponse("dicks")