Hi, to make everyones lives easier ive made a cheatsheet on how you should implement our permissions for when youre writing your forms or htmls

So, the general syntax for our permissions is  `<app>.<permission>` or for a more concrete example, as out app is always going to be manager `'manager.is_a_captain'` which is our global permission just to check if a user is a captain of any team.

## Code Usage

### Global Permissions
```python
if request.user.has_perm(manager.<permission>):
	pass
```  


##### @permission_required decorator
Please remember to add the raise_exception=True argument so it doesnt send you to the login page

e.g ` @permission_required('manager.is_a_captain', raise_exception=True) `

## HTML Usage

First of all please use ` {% load guardian_tags %} ` please

Remember, as only users with the "is_a_captain" permission can access this, they logically must be their captain as they only captain one team.
If you are letting them input their own team name this validation works: 

```
{% if Team.object.get(team_name = <teamname>) == request.user.registered_team%}

{% endif %}
```

Otherwise you can exploit that you can get the users team, and not even let them input their team name, simply ask what team they want to challenge, you can just chuck this in for your context dictionary 
```python
current_player = Player.objects.get(username=request.user.username)  
context['Team'] = Team.objects.get(team_name = current_player.registered_team)
```

You now dont even need to do any authentication code html side, as the permissions check has already happened
