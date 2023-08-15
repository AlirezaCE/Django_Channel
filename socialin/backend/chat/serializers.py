from user.serializers import UserUsernameSerializer
from .models import Conversation, Message
from rest_framework import serializers

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ('conversation_id',)


class ConversationListSerializer(serializers.ModelSerializer):
    initiator = UserUsernameSerializer(read_only=True)
    receiver = UserUsernameSerializer()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id','initiator', 'receiver', 'last_message']

    def get_last_message(self, instance):
        last_message = instance.message_set.first()
        if last_message:
            return MessageSerializer(instance=last_message).data
        return None

class ConversationSerializer(serializers.ModelSerializer):
    initiator = UserUsernameSerializer(read_only=True)
    receiver = UserUsernameSerializer()
    message_set = MessageSerializer(many=True)

    class Meta:
        model = Conversation
        fields = ['initiator', 'receiver', 'message_set']