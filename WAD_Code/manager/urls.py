from django.urls import path
from manager import views

app_name = 'manager'

urlpatterns = [
    path('', views.index, name='index'),
    #path('profile/', views.profile, name='profile'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('search_teams/', views.search_teams, name="search_teams"),
    path('search_teams/<slug:team_name>/', views.view_team, name="view_team"),
    #path('search_results/<str:search>', views.search_results, name="search_results"),
    path('search_results/', views.search_teams, name="search_results"),
    path('signup/team/', views.signup_team, name="signup_team"),
    path('signup/individual/', views.signup_individual, name='signup_individual'),
    path('login/', views.user_login, name='login'),
    # path('login/<slug:team_name>/', views.team_account, name="team_account"),
    # path('login/<slug:user_name>/', views.individual_account, name="individual_account"),
    path('logout/', views.user_logout, name='logout'),
    path('search_teams/<slug:team_name>/match_request/', views.request_match, name='request_match'),
    path('contact/', views.contact_us, name='contact'),
    path('faq/', views.faq, name='faq')
]