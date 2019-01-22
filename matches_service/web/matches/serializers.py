from rest_framework import serializers

from matches.models import Match, Invite


class MatchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'


class InviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = '__all__'
