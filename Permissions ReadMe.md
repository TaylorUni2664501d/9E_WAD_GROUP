Hi, to make everyones lives easier ive made a cheatsheet on how you should implement our permissions for when youre writing your forms or htmls

So, the general syntax for our permissions is  `<app>.<permission>` or for a more concrete example, as out app is always going to be manager `'manager.is_a_captain'` which is our global permission just to check if a user is a captain of any team.

## Code Usage

### Global Permissions
```python
if request.user.has_perm(manager.<permission>):
	pass
```  

### Local/Object Specific Permissions

```python
#If the team relevant for the permissions isnt already defined
current_player = Player.objects.get(username=request.user.username)  
the_team_name = current_player.registered_team
team = Team.objects.get(team_name = the_team_name)
# Im not fully sure if registered_team connects to team_name or some id, this assumes it connects to a team_name 

if request.user.has_perm(manager.<permission>, team):
	pass
```  

##### @permission_required decorator
This field for now is only capable of taking global permissions, but please remember to add the raise_exception=True argument so it doesnt send you to the login page

e.g ` @permission_required('manager.is_a_captain', raise_exception=True) `

## HTML Usage

First of all please use ` {% load guardian_tags %} ` please

First of all, outside your template, you should try use this code to get a list of all the team objects a user is captain to. This can then be compared against for authentication or what not
```python
from guardian.shortcuts import get_objects_for_user
...
teams_captained = get_objects_for_user(request.user, "captain_perms", Team.objects.all())

context['captained_teams'] = teams_captained
```

```
{% if Team.object.get(team_name = <teamname>) in captained_teams %}

{% endif %}
```
