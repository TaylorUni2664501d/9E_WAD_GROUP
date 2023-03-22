from django.db import models
from django.contrib.auth.models import User
from WAD_Code.settings import STATIC_DIR
from django.template.defaultfilters import slugify

# Create your models here.

# COLLECTED DOCUMENTATION ON IMPORTANT FIELDS AND PARAMETERS NOT USED IN RANGO
# DateField: https://docs.djangoproject.com/en/2.1/ref/models/fields/#datefield
# ImageField: https://docs.djangoproject.com/en/2.1/ref/models/fields/#imagefield
# ManyToManyField: https://docs.djangoproject.com/en/2.1/ref/models/fields/#manytomanyfield
# Choices: https://docs.djangoproject.com/en/2.1/ref/models/fields/#choices



# helper method to name and organise team logos
# MUST BE OUTSIDE CLASS - DJANGO SPECIFIC IMPLEMENTATION
def logo_directory_path(instance, filename):
    return f"team_logo/team_{instance.team_name}/{filename}"
class Team(models.Model):
    #REDUNDANT METHOD - DO NOT REMOVE IT BREAKS EVERYTHING
    def gallery_default(self): #helper method to make a per-entry default value pointing to the team's gallery folder - ideally should not need changed
        return f"team_gallery/team_{self.team_name}/"

    team_name = models.CharField(max_length=64, unique=True)
    team_password = models.CharField(max_length=32, default="defaultPassword")
    location = models.CharField(max_length=64)
    age_range = models.CharField(max_length=5)
    win_rate = models.FloatField(default=0.0)
    bio = models.TextField(max_length=500)
    logo = models.ImageField(upload_to=f"team_logo/") # TODO: Fix logo upload
    gallery = models.CharField(max_length=200, default=f"team_gallery/team_{team_name}/") # currently just using a string for the folder path, no better field type exists
    slug = models.SlugField(unique=True, default="error")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.team_name)
        self.team_password = hash(self.team_password) # save the hash of the password - not plaintext
        super(Team, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.team_name}"

    #Permissions code for teams
    class Meta:
        permissions = (("is_a_captain", "Standard Captain Permissions"), ("is_a_player", "Standard Player Permissions"),)

# helper method to name and organise user profile pictures
# MUST BE OUTSIDE CLASS - DJANGO SPECIFIC IMPLEMENTATION
def user_directory_path(instance, filename):
    return f"player_profile_pic/user_{instance.id}/{filename}"

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=0)
    # Forename and Surname gotten from User
    age = models.IntegerField(default=0)
    location = models.CharField(max_length=64)
    bio = models.TextField(max_length=500)
    # image fields allow users to enter an image in the form, and have it automatically uploaded to the correct media directory
    # https://docs.djangoproject.com/en/2.1/ref/models/fields/#imagefield
    profile_pic = models.ImageField(upload_to=user_directory_path, default=f"images/default_profile.jpeg")
    registered_team = models.ForeignKey(Team, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Match(models.Model):
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="+") #challenging team
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="+") #challenged team
    date = models.DateField()
    pitch = models.CharField(max_length=64)
    winner = models.IntegerField(blank=True, default="0") # the ID of the winning team - left null at creation, added after match resolution
    loser = models.IntegerField(blank=True, default="0")
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
        return f"{self.team1} vs {self.team2} at {self.date}"

class Team_Request(models.Model):
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE) # may not need to be foreign key, unsure as it should reference an id, implementation should work regardless
    date_made = models.DateField()

    def __str__(self):
        return f"Request {self.player_id} to team {self.team_id}"