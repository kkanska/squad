from django.http import HttpResponse
from django.http import Http404

from rest_framework.views import APIView

from django.contrib.gis.geos import Point
from rest_framework.response import Response
from rest_framework import status

from matches.models import Match, Invite
from matches.serializers import MatchesSerializer, InviteSerializer

import datetime

from .forms import GenerateRandomMatchesForm
from .tasks import create_match
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.contrib import messages
from django.shortcuts import redirect

import random

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

class NewMatchesList(ListView):
    template_name = 'matches/new_matches_list.html'
    model = Match
    paginate_by = 10
    queryset = Match.objects.all().order_by('date', '-location')


# from dateutil.parser import parse

class GenerateRandomMatchesView(FormView):
    template_name = 'matches/generate_random_matches.html'
    form_class = GenerateRandomMatchesForm

    def form_valid(self, form):
        playground_latitude = form.cleaned_data['playground_latitude']
        playground_longitude = form.cleaned_data['playground_longitude']
        author_id = form.cleaned_data['author_id']
        start_hour = form.cleaned_data['playing_from_hour']
        end_hour = form.cleaned_data['playing_to_hour']
        start_date_str = form.cleaned_data['playing_from_date']
        end_date_str = form.cleaned_data['playing_to_date']
        match_length = form.cleaned_data['one_match_length_in_minutes']
        players = set(form.cleaned_data['players'].replace(',', ' ').split())
        discipline = form.cleaned_data['discipline']
        start_date = start_date_str
        end_date = end_date_str

        all_matches = []
        for day_num in range(int((end_date - start_date).days) + 1):
            for time in range(int((end_hour - start_hour)*60/match_length)):
                match_date = start_date + datetime.timedelta(day_num)
                match_start = start_hour*60 + time*match_length
                match_end = match_start + match_length
                if len(players) > 12:
                    squad_size = 12
                else:
                    squad_size = len(players) - len(players)%2
                match_squad = random.sample(players, squad_size)
                all_matches.append({
                    "point": (playground_latitude, playground_longitude),
                    "author_id": author_id,
                    "date": datetime.datetime.combine(match_date, datetime.datetime.min.time()),
                    "minute_start": match_start,
                    "minute_end": match_end,
                    "squad": match_squad,
                    "discipline": discipline
                })
        for match in all_matches:
            create_match.delay(match)

        return redirect('new_matches_list')


def clear_db(request):
    Match.objects.all().delete()
    return redirect('new_matches_list')