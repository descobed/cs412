import json
import os
from datetime import timedelta
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Max, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import CreateView, DetailView, TemplateView, View

from .forms import CreateProfileForm, CreateReviewForm
from .models import Album, Artist, Friend, Profile, Review, Song


class HomeView(TemplateView):
    """View for showing the home page."""

    template_name = 'musicBlog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recent_cutoff = timezone.now() - timedelta(days=30)
        context['recent_top_albums'] = Album.objects.filter(
            review__created_at__gte=recent_cutoff,
        ).annotate(
            recent_rater_count=Count('review__profile', distinct=True),
            latest_recent_review=Max('review__created_at'),
        ).order_by('-recent_rater_count', '-latest_recent_review', 'title')[:5]

        user = self.request.user
        if user.is_authenticated:
            profile = Profile.objects.filter(user=user).first()
            if profile:
                friend_profile_ids = Friend.objects.filter(
                    profile=profile
                ).values_list('friend_profile_id', flat=True)
                context['home_friend_reviews'] = Review.objects.filter(
                    profile_id__in=friend_profile_ids,
                ).select_related('album', 'album__artist', 'profile').order_by('-created_at')[:10]
            else:
                context['home_friend_reviews'] = Review.objects.none()
        return context


class ProfileDetailView(LoginRequiredMixin, DetailView):
    """View for showing a profile."""

    model = Profile
    template_name = 'musicBlog/profile_detail.html'
    context_object_name = 'profile'

    def get_object(self):
        return Profile.objects.filter(user=self.request.user).first()

    def get_login_url(self):
        return reverse('musicBlog:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object is not None:
            friendships = self.object.get_friends()
            friend_profile_ids = friendships.values_list('friend_profile_id', flat=True)

            context['friendships'] = friendships
            context['friend_reviews'] = Review.objects.filter(
                profile_id__in=friend_profile_ids,
            ).select_related('album', 'album__artist', 'profile').order_by('-created_at')
        else:
            context['friendships'] = Profile.objects.none()
            context['friend_reviews'] = Review.objects.none()
        return context


class AddFriendView(LoginRequiredMixin, View):
    """Create a friend relationship for the logged-in user's profile."""

    def get_login_url(self):
        return reverse('musicBlog:login')

    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user=request.user)
        friend_profile = get_object_or_404(Profile, pk=request.POST.get('friend_profile_pk'))

        if friend_profile != profile:
            Friend.objects.get_or_create(profile=profile, friend_profile=friend_profile)

        next_url = request.POST.get('next', '').strip()
        if next_url:
            return redirect(next_url)
        return redirect(reverse('musicBlog:show_profile'))


class RemoveFriendView(LoginRequiredMixin, View):
    """Remove a friend relationship for the logged-in user's profile."""

    def get_login_url(self):
        return reverse('musicBlog:login')

    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user=request.user)
        friend_profile = get_object_or_404(Profile, pk=request.POST.get('friend_profile_pk'))

        Friend.objects.filter(profile=profile, friend_profile=friend_profile).delete()

        next_url = request.POST.get('next', '').strip()
        if next_url:
            return redirect(next_url)
        return redirect(reverse('musicBlog:show_profile'))


class FindFriendsView(LoginRequiredMixin, TemplateView):
    """Find profiles to add as friends."""

    template_name = 'musicBlog/find_friends.html'

    def get_login_url(self):
        return reverse('musicBlog:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.filter(user=self.request.user).first()
        query = self.request.GET.get('q', '').strip()

        context['q'] = query
        context['search_results'] = Profile.objects.none()
        context['profile'] = profile

        if profile is None:
            return context

        existing_friend_ids = Friend.objects.filter(profile=profile).values_list('friend_profile_id', flat=True)
        context['existing_friend_ids'] = set(existing_friend_ids)

        candidates = Profile.objects.exclude(pk=profile.pk)
        if query:
            candidates = candidates.filter(
                Q(username__icontains=query) | Q(display_name__icontains=query)
            )

        context['search_results'] = candidates.order_by('display_name', 'username')
        return context


class FriendProfileDetailView(LoginRequiredMixin, DetailView):
    """Display a friend's profile page and reviews."""

    model = Profile
    template_name = 'musicBlog/friend_profile_detail.html'
    context_object_name = 'friend_profile'

    def get_login_url(self):
        return reverse('musicBlog:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.review_set.select_related('album').order_by('-created_at')
        return context

class DiscogsSearchView(LoginRequiredMixin, TemplateView):
    """Search Discogs for artists, albums, and songs in separate sections."""

    template_name = 'musicBlog/discogs_search.html'
    discogs_base_url = 'https://api.discogs.com/database/search'

    def get_login_url(self):
        return reverse('musicBlog:login')

    def _fetch(self, query, search_type, headers):
        """Return discog search"""
        params = {'q': query, 'type': search_type, 'per_page': 5, 'page': 1}
        endpoint = f"{self.discogs_base_url}?{urlencode(params)}"
        try:
            req = Request(endpoint, headers=headers)
            with urlopen(req, timeout=10) as resp:
                payload = json.loads(resp.read().decode('utf-8'))
            return payload.get('results', [])[:5], ''
        except HTTPError as exc:
            return [], f'Discogs request failed ({exc.code}).'
        except URLError:
            return [], 'Could not reach Discogs. Please try again.'
        except (json.JSONDecodeError, TimeoutError):
            return [], 'Discogs returned an invalid response.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '').strip()
        context['q'] = query
        context['artist_results'] = []
        context['album_results'] = []
        context['song_results'] = []
        context['artist_error'] = ''
        context['album_error'] = ''
        context['song_error'] = ''

        if not query:
            return context

        headers = {'User-Agent': 'MusicBlog/1.0 (+https://example.com)'}
        user_token = os.getenv('DISCOGS_USER_TOKEN', '').strip()
        if user_token:
            headers['Authorization'] = f'Discogs token={user_token}'

        context['artist_results'], context['artist_error'] = self._fetch(query, 'artist', headers)
        context['album_results'], context['album_error'] = self._fetch(query, 'release', headers)
        context['song_results'], context['song_error'] = self._fetch(query, 'track', headers)

        return context


class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'musicBlog/create_profile_form.html'

    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)
        user = user_form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        form.instance.user = user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_creation_form'] = UserCreationForm()
        return context

    def get_success_url(self):
        return reverse('musicBlog:show_profile')


class AlbumDetailView(DetailView):
    """Show an album and all its reviews."""

    model = Album
    template_name = 'musicBlog/album_detail.html'
    context_object_name = 'album'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.get_reviews()
        context['songs'] = self.object.get_songs()
        return context


class ArtistDetailView(DetailView):
    """Show an artist with all albums and songs."""

    model = Artist
    template_name = 'musicBlog/artist_detail.html'
    context_object_name = 'artist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['albums'] = self.object.get_albums().order_by('release_date', 'title')
        context['songs'] = Song.objects.filter(album__artist=self.object).select_related('album').order_by('album__title', 'title')
        return context


class CreateReviewView(LoginRequiredMixin, CreateView):
    """Create a review for an album, attached to the logged-in user's profile."""

    model = Review
    form_class = CreateReviewForm
    template_name = 'musicBlog/create_review_form.html'

    def get_login_url(self):
        return reverse('musicBlog:login')

    def get_album(self):
        return Album.objects.get(pk=self.kwargs['album_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['album'] = self.get_album()
        return context

    def form_valid(self, form):
        form.instance.album = self.get_album()
        form.instance.profile = Profile.objects.filter(user=self.request.user).first()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('musicBlog:album_detail', kwargs={'pk': self.kwargs['album_pk']})


class SaveAndReviewView(LoginRequiredMixin, View):
    """Save a Discogs result as a local Album (get_or_create) then redirect to review form."""

    def get_login_url(self):
        return reverse('musicBlog:login')

    def resolve_artist(self, raw_artist_name, genre=''):
        """Create or fetch the local artist matching a search result."""
        artist_name = (raw_artist_name or 'Unknown Artist').strip()
        artist, _ = Artist.objects.get_or_create(
            name=artist_name,
            defaults={'genre': genre},
        )
        return artist

    def resolve_album(self, raw_title, year, genre):
        """Local items vs dicogs result, Lowk really messy :("""
        if ' - ' in raw_title:
            artist_name, album_title = raw_title.split(' - ', 1)
        else:
            artist_name = 'Unknown Artist'
            album_title = raw_title or 'Unknown Album'

        artist = self.resolve_artist(artist_name, genre)

        release_date = None
        if year and year.isdigit():
            release_date = f'{year}-01-01'

        album, _ = Album.objects.get_or_create(
            title=album_title.strip(),
            artist=artist,
            defaults={'genre': genre, 'release_date': release_date},
        )
        return album

    def post(self, request, *args, **kwargs):
        raw_title = request.POST.get('title', '').strip()
        year = request.POST.get('year', '').strip()
        genre = request.POST.get('genre', '').strip()

        album = self.resolve_album(raw_title, year, genre)

        return redirect(reverse('musicBlog:create_review', kwargs={'album_pk': album.pk}))


class SaveAndViewAlbumView(SaveAndReviewView):
    """Save a Discogs result as a local Album (get_or_create) then redirect to album detail."""

    def _fetch_release_data(self, resource_url):
        """Return release data from Discogs API, or {} on error."""
        if not resource_url:
            return {}
        headers = {'User-Agent': 'MusicBlog/1.0 (+https://example.com)'}
        user_token = os.getenv('DISCOGS_USER_TOKEN', '').strip()
        if user_token:
            headers['Authorization'] = f'Discogs token={user_token}'
        try:
            req = Request(resource_url, headers=headers)
            with urlopen(req, timeout=10) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except (HTTPError, URLError, json.JSONDecodeError, TimeoutError):
            return {}

    def _fetch_tracks(self, release_data):
        """Return the tracklist from release data, or []."""
        return release_data.get('tracklist', [])

    def _parse_duration(duration_str):
        """Fix the time dicreponcy """
        if not duration_str:
            return None
        parts = duration_str.split(':')
        try:
            if len(parts) == 2:
                return int(parts[0]) * 60 + int(parts[1])
            if len(parts) == 1:
                return int(parts[0])
        except ValueError:
            pass
        return None

    def post(self, request, *args, **kwargs):
        raw_title = request.POST.get('title', '').strip()
        year = request.POST.get('year', '').strip()
        genre = request.POST.get('genre', '').strip()
        resource_url = request.POST.get('resource_url', '').strip()
        album = self.resolve_album(raw_title, year, genre)

        if resource_url:
            release_data = self._fetch_release_data(resource_url)
            
            # Fetch and save tracks if we don't have any
            if not album.get_songs().exists():
                for track in release_data.get('tracklist', []):
                    title = track.get('title', '').strip()
                    if title:
                        Song.objects.get_or_create(
                            title=title,
                            album=album,
                            defaults={'length': self._parse_duration(track.get('duration', ''))},
                        )

        return redirect(reverse('musicBlog:album_detail', kwargs={'pk': album.pk}))


class SaveAndViewArtistView(SaveAndReviewView):
    """Save an artist search result locally (get_or_create) then redirect to artist detail."""

    def post(self, request, *args, **kwargs):
        raw_artist_name = request.POST.get('artist_name', '').strip()
        genre = request.POST.get('genre', '').strip()
        artist = self.resolve_artist(raw_artist_name, genre)
        return redirect(reverse('musicBlog:artist_detail', kwargs={'pk': artist.pk}))

    
