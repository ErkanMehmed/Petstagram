from copy import copy

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import OuterRef, Exists
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, resolve_url
from django.views.generic import ListView

from photos.models import Photo

from common.models import Like

from common.forms import SearchForm, CommentForm


class HomePageView(ListView):
    template_name = 'common/home-page.html'
    context_object_name = 'all_photos'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['search_form'] = SearchForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = Photo.objects.prefetch_related('tagged_pets', 'like_set').order_by('-date_of_publication')
        pet_name = self.request.GET.get('pet_name')

        if pet_name:
            queryset = queryset.filter(tagged_pets__name__icontains=pet_name)

        if self.request.user.is_authenticated:
            queryset = queryset.annotate(is_liked_by_user=Exists(Like.objects.filter(to_photo_id=OuterRef('pk'), user=self.request.user,)))
        else:
            queryset = queryset.annotate(is_liked_by_user=Exists(Like.objects.none()),)

        return queryset

@login_required
def like_functionality_view(request: HttpRequest, photo_pk: int) -> HttpResponse:
    like_object = Like.objects.filter(to_photo_id=photo_pk, user=request.user).first()

    if like_object:
        like_object.delete()
    else:
        Like.objects.create(to_photo_id=photo_pk, user=request.user,)

    return redirect(request.META.get('HTTP_REFERER') + '#{photo_pk}')

@login_required
def add_comment_view(request: HttpRequest, photo_pk: int) -> HttpResponse:
    if request.method == 'POST':
        photo = Photo.objects.get(pk=photo_pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.to_photo = photo
            comment.user = request.user
            comment.save()

        return redirect(request.META.get('HTTP_REFERER') + '#{photo_pk}')

def share_functionality(request: HttpRequest, photo_pk: int) -> HttpResponse:
    copy(request.META.get('HTTP_REFERER')[:-1] + resolve_url('photos:details', photo_pk))
    return redirect(request.META.get('HTTP_REFERER') + '#{photo_pk}')

def show_home_page(request):
    all_photos = Photo.objects.all()
    comment_form = CommentForm()
    search_form = SearchForm()

    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            all_photos = all_photos.filter(tagged_pets__name__icontains=search_form.cleaned_data['pet_name'])

    photos_per_page = 1
    paginator = Paginator(all_photos, photos_per_page)
    page = request.GET.get('page')

    try:
        all_photos = paginator.page(page)
    except PageNotAnInteger:
        all_photos = paginator.page(1)
    except EmptyPage:
        all_photos = paginator.page(paginator.num_pages)
