from summoners.models import Summoner, LadderStanding

def select_by_riotid(*, name: str, tag_line: str):
    query = Summoner.objects.filter(game_name__iexact=name, tag_line__iexact=tag_line)
    if not query.exists():
        return None
    return query

def select_standing_by_summoner(*, local_summoner_id: int):
    query = LadderStanding.objects.filter(belongs_to=local_summoner_id)
    if not query.exists():
        return None
    return query