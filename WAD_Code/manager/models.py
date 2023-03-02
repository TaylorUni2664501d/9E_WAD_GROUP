from django.db import models

# Create your models here.

# COLLECTED DOCUMENTATION ON IMPORTANT FIELDS AND PARAMETERS NOT USED IN RANGO
# DateField: https://docs.djangoproject.com/en/2.1/ref/models/fields/#datefield
# ImageField: https://docs.djangoproject.com/en/2.1/ref/models/fields/#imagefield
# ManyToManyField: https://docs.djangoproject.com/en/2.1/ref/models/fields/#manytomanyfield
# Choices: https://docs.djangoproject.com/en/2.1/ref/models/fields/#choices

# helper method to name and organise user profile pictures 
# MUST BE OUTSIDE CLASS - DJANGO SPECIFIC IMPLEMENTATION
def user_directory_path(instance, filename):
    return f"player_profile_pic/user_{instance.id}/{filename}"
class Player(models.Model):
    forename = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    age = models.IntegerField(default=0)
    location = models.CharField(max_length=64)
    bio = models.TextField(max_length=500)
    # image fields allow users to enter an image in the form, and have it automatically uploaded to the correct media directory
    # https://docs.djangoproject.com/en/2.1/ref/models/fields/#imagefield
    profile_pic = models.ImageField(upload_to=user_directory_path)

    def __str__(self):
        return f"{self.forename} {self.surname}"

# helper method to name and organise team logos
# MUST BE OUTSIDE CLASS - DJANGO SPECIFIC IMPLEMENTATION
def logo_directory_path(instance, filename):
    return f"team_logo/team_{instance.team_name}/{filename}"
class Team(models.Model):
    def gallery_default(self): #helper class to make a per-entry default value pointing to the team's gallery folder - ideally should not need changed
        return f"team_gallery/team_{self.team_name}/"
    
    team_name = models.CharField(max_length=64, unique=True)
    # many-to-many field via Team_Players, allows Team to contain players and hopefully simplify implementation while keeping extra relationship data
    # https://docs.djangoproject.com/en/2.1/ref/models/fields/#manytomanyfield
    registered_players = models.ManyToManyField( 
        Player,
        through="Team_Players",
        through_fields=("team_id", "player_id")
    )
    location = models.CharField(max_length=64)
    age_range = models.CharField(max_length=5)
    win_rate = models.FloatField(default=0.0)
    bio = models.TextField(max_length=500)
    logo = models.ImageField(upload_to=logo_directory_path)
    gallery = models.CharField(max_length=200, default=gallery_default) # currently just using a string for the folder path, no better field type exists

    def __str__(self):
        return f"{self.team_name}"

class Match(models.Model):
    team1_id = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="+") #challenging team
    team2_id = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="+") #challenged team
    date = models.DateField()
    pitch = models.CharField(max_length=64)
    winner = models.IntegerField() # the ID of the winning team - left null at creation, added after match resolution
    loser = models.IntegerField()
    # defined status, forcing field to only contain set options, preventing input-based errors
    # https://docs.djangoproject.com/en/2.1/ref/models/fields/#choices
    STATUS_CHOICES = (
        ("AC", "Accepted"),
        ("PN", "Pending"),
        ("DN", "Denied"),
        ("CM", "Complete")
    )
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default="PN")

    def __str__(self):
        return f"{self.team1_id} vs {self.team2_id}"

class Team_Players(models.Model): # many-to-many intermediary table
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE)
    date_joined = models.DateField()

    def __str__(self):
        return f"{self.team_id} player {self.player_id}"

class Team_Request(models.Model):
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE) # may not need to be foreign key, unsure as it should reference an id, implementation should work regardless
    date_made = models.DateField()

    def __str__(self):
        return f"Request {self.player_id} to team {self.team_id}"