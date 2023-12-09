from django.conf import settings
from summoners.models import Summoner, LadderStanding
from summoners.logic import selectors
import requests

ACCOUNT_BY_RIOT_ID = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id"
# Bro what the fuck is this convoluted web of nonsense fuck 
SUMMONER_ID_BY_PUUID = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid"
# This shit might include all queues? e.g solo/flex, but I'm not a fucking pussy so don't have flex games.
# If this breaks with some users, it's darwinism and shouldn't be fixed. 
RANKED_BY_SUMMONER_ID = "https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner"
MATCH_IDS_BY_PUUID = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid"
MATCH_BY_ID = "https://americas.api.riotgames.com/lol/match/v5/matches"

def get_puuid_by_riotid(*, name: str, tag_line: str):
    url = f"{ACCOUNT_BY_RIOT_ID}/{name}/{tag_line}"
    r = requests.get(url, headers={"X-Riot-Token": settings.RIOT_API_KEY})
    return r.json()

def get_match_ids_by_puuid(*, puuid: str):
    url = f"{MATCH_IDS_BY_PUUID}/{puuid}"
    r = requests.get(url, headers={"X-Riot-Token": settings.RIOT_API_KEY})
    return r.json()

def get_match_by_id(*, id: str):
    url = f"{MATCH_BY_ID}/{id}"
    r = requests.get(url, headers={"X-Riot-Token": settings.RIOT_API_KEY})
    return r.json()

def get_summonerid_by_puuid(*, puuid: str):
    url = f"{SUMMONER_ID_BY_PUUID}/{puuid}"
    r = requests.get(url, headers={"X-Riot-Token": settings.RIOT_API_KEY})
    return r.json()

def get_ranked_by_summonerid(*, summoner_id: str):
    url = f"{RANKED_BY_SUMMONER_ID}/{summoner_id}"
    r = requests.get(url, headers={"X-Riot-Token": settings.RIOT_API_KEY})
    return r.json()

def start_tracking(*, name: str, tag_line: str):
    puuid_resp = get_puuid_by_riotid(name=name, tag_line=tag_line)
    summoner = commit_summoner(puuid=puuid_resp.get("puuid"), name=name, tag_line=tag_line)
    standing = commit_ladder_standing(local_summoner_id=summoner.id, summoner_id=summoner.summoner_id)

def commit_summoner(*, puuid: str, name: str, tag_line: str) -> Summoner:
    resp = get_summonerid_by_puuid(puuid=puuid)
    insertion = Summoner.objects.create(
        puuid=puuid, game_name=name, tag_line=tag_line,
        profile_icon=resp.get("profileIconId"), summoner_id=resp.get("id"),
        level=resp.get("summonerLevel"), account_id=resp.get("accountId"))
    # I think Django is iffy here. `Summoner.objects.create()` shouldn't require a subsequent call to `.save()`,
    # but if I were to `insertion = Summoner(puuid=puuid, ...etc)`, I'd then be forced to call `.save()`? Aids~ >_<
    return insertion

def commit_ladder_standing(*, local_summoner_id: int, summoner_id: str):
    imgay = selectors.select_standing_by_summoner(local_summoner_id=local_summoner_id)
    if imgay is not None:
        return None

    summoner = Summoner.objects.get(id=local_summoner_id)
    resp = get_ranked_by_summonerid(summoner_id=summoner.summoner_id)
    for queue in resp:
        insertion = LadderStanding.objects.create(
            belongs_to=summoner, league_id=queue.get("leagueId"), queue_type=queue.get("queueType"),
            tier=queue.get("tier"), rank=queue.get("rank"), lp=queue.get("leaguePoints"),
            wins=queue.get("wins"), losses=queue.get("losses"), veteran=queue.get("veteran"),
            inactive=queue.get("inactive"), fresh_blood=queue.get("freshBlood"), hot_streak=queue.get("hotStreak"))