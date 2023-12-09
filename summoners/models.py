from django.db import models


class Summoner(models.Model):
    puuid = models.CharField(unique=True, max_length=200)
    game_name = models.CharField(max_length=32)
    tag_line = models.CharField(max_length=5)   # it's 5 I think?
    profile_icon = models.IntegerField(default=0)
    account_id = models.CharField(max_length=200, unique=True)
    # ?
    summoner_id = models.CharField(max_length=200, unique=True)
    level = models.IntegerField(default=1)
    first_seen = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.game_name} #{self.tag_line}"


class LadderStanding(models.Model):
    belongs_to = models.ForeignKey(Summoner, on_delete=models.CASCADE)
    league_id = models.CharField(max_length=400)
    queue_type = models.CharField(max_length=69)
    tier = models.CharField(max_length=40)
    rank = models.CharField(max_length=3)
    lp = models.IntegerField()
    wins = models.IntegerField()
    losses = models.IntegerField()
    # What the fuck do these even mean???
    veteran = models.BooleanField()
    fresh_blood = models.BooleanField()
    # --
    inactive = models.BooleanField()
    hot_streak = models.BooleanField()
    first_seen = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.belongs_to} | {self.queue_type} - {self.tier} {self.rank} {self.lp}LP"