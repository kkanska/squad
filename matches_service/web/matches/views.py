from django.http import HttpResponse
from django.http import Http404

from rest_framework.views import APIView

from django.contrib.gis.geos import Point
from rest_framework.response import Response
from rest_framework import status

from matches.models import Match, Invite
from matches.serializers import MatchesSerializer, InviteSerializer

import datetime


class MatchesList(APIView):
    def get(self, request, format=None):
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
        distance = request.GET.get('radius')
        author = request.GET.get('author')
        date = request.GET.get('date')
        players = request.GET.getlist('player')

        matches = Match.objects.all()

        if lat and lng and distance:
            point = Point(float(lng), float(lat))
            matches = matches.filter(location__distance_lt=(point, distance))
        elif lat or lng or distance:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        if author:
            matches = matches.filter(author_id=int(author))

        if date:
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            matches = matches.filter(date=date)

        if players:
            matches = matches.filter(players__contains=players)

        serializer = MatchesSerializer(matches, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        json = request.data
        serializer = MatchesSerializer(data=json)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, format=None):
        id = request.data['id']
        new_player = request.data.get('new_player')
        remove_player = request.data.get('player_to_remove')

        match = Match.objects.get(id=id)
        if new_player:
            match.players.append(int(new_player))
        elif remove_player:
            match.players.remove(int(new_player))
        else:
            HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        match.save()
        serializer = MatchesSerializer(match)

        return Response(serializer.data, status=status.HTTP_200_OK)


class MatchDetails(APIView):
    def get_object(self, pk):
        try:
            return Match.objects.get(pk=pk)
        except Match.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = MatchesSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = MatchesSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class InvitesList(APIView):
    def get(self, request):
        match = request.GET.get('match')
        inviter = request.GET.get('inviter')
        invitee = request.GET.get('invitee')

        invites = Invite.objects.all()

        if match:
            invites = invites.filter(match__id=int(match))
        if inviter:
            invites = invites.filter(inviter=int(inviter))
        if invitee:
            invites = invites.filter(invitee=int(invitee))

        serializer = InviteSerializer(invites, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        json = request.data
        serializer = InviteSerializer(data=json)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
