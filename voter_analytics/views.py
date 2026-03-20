from django.db.models import Count
from django.db.models.functions import ExtractYear #NOTICE
from .models import Voter
from django.views.generic import ListView, DetailView

import plotly
import plotly.graph_objs as go

# Create your views here.


def query_voter_data(qs, params):
    """Reused in both search and graph so taken out as a helper
    Might be a better way to do this
    """

    party_affiliation = params.get('party_affiliation', '').strip()
    if party_affiliation:
        qs = qs.filter(party_affiliation__icontains=party_affiliation)

    min_dob = params.get('min_dob', '').strip()
    if min_dob:
        qs = qs.filter(dob__gte=min_dob)

    max_dob = params.get('max_dob', '').strip()
    if max_dob:
        qs = qs.filter(dob__lte=max_dob)

    voter_score = params.get('voter_score', '').strip()
    if voter_score:
        qs = qs.filter(voter_score=voter_score)

    if params.get('v20state'):
        qs = qs.filter(v20state='TRUE')

    if params.get('v21city'):
        qs = qs.filter(v21city='TRUE')

    if params.get('v21primary'):
        qs = qs.filter(v21primary='TRUE')

    if params.get('v22general'):
        qs = qs.filter(v22general='TRUE')

    if params.get('v23town'):
        qs = qs.filter(v23town='TRUE')

    return qs

class VoterListView(ListView):
    '''See (100) voters'''

    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        result = super().get_queryset()
        return query_voter_data(result, self.request.GET)

    #Notice
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET.copy()
        query_params.pop('page', None)
        context['current_query'] = query_params.urlencode()
        return context
     

class VoterDetailView(DetailView):
    '''See 1 detail voter'''

    template_name = 'voter_analytics/voter_detail.html'
    model = Voter
    context_object_name = 'voter'

    def get_context_data(self, **kwargs):
        '''Context for the detail view'''
        
        context = super().get_context_data(**kwargs)
        return context
    

class GraphListView(ListView):
    '''See graphs'''

    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'voters'

    Parties = ['CC', 'U', 'R', 'D']

    def get_queryset(self):
        result = super().get_queryset()
        return query_voter_data(result, self.request.GET)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voters = context['voters']

        party_rows = voters.values('party_affiliation').annotate(count=Count('party_affiliation'))
        party_counts_map = {}
        for row in party_rows:
            party = (row['party_affiliation'] or '').strip()
            if party in self.Parties:
                party_counts_map[party] = row['count']

        party_counts = [party_counts_map.get(party, 0) for party in self.Parties]

        graph_pie = go.Figure(data=[go.Pie(labels=self.Parties, values=party_counts)])
        graph_pie.update_layout(title='Distribution of Voters by Party Affiliation')

        voters_by_year = (
            voters
            .annotate(year=ExtractYear('dob'))
            .values('year')
            .annotate(count=Count('id'))
            .order_by('year')
        )
        years = [row['year'] for row in voters_by_year if row['year'] is not None]
        yearly_counts = [row['count'] for row in voters_by_year if row['year'] is not None]

        graph_bar_year = go.Figure(data=[go.Bar(x=years, y=yearly_counts)])
        graph_bar_year.update_layout(
            title='Number of Voters per DOB',
            xaxis_title='Year',
            yaxis_title='Number of Voters'
        )

        election_labels = [
            '2020 State',
            '2021 Town',
            '2021 Primary',
            '2022 General',
            '2023 Town',
        ]
        election_counts = [
            voters.filter(v20state='TRUE').count(),
            voters.filter(v21city='TRUE').count(),
            voters.filter(v21primary='TRUE').count(),
            voters.filter(v22general='TRUE').count(),
            voters.filter(v23town='TRUE').count(),
        ]
        graph_bar_election = go.Figure(data=[go.Bar(x=election_labels, y=election_counts)])
        graph_bar_election.update_layout(
            title='Voters per election',
            xaxis_title='Election',
            yaxis_title='Number of Voters'
        )

        context['graph_div_pie'] = plotly.offline.plot(graph_pie, output_type='div')
        context['graph_div_bar_election_count'] = plotly.offline.plot(graph_bar_election, output_type='div')
        context['graph_div_bar_dob'] = plotly.offline.plot(graph_bar_year, output_type='div')


        return context
