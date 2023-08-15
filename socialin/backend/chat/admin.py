from django.contrib import admin
from .models import *


class ConversationModel(admin.ModelAdmin):
    list_display = ('id','initiator', 'receiver','start_time')


admin.site.register(Conversation, ConversationModel)
admin.site.register(Message)
