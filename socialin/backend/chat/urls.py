from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.StartConversationView.as_view(), name = 'start_convo'),
    path('<int:id>/', views.GetConversationView.as_view(), name = 'get_conversation'),
    path('conversations/', views.ConversationsListView.as_view(), name = 'conversations')
]