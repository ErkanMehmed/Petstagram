from django.db.models import Prefetch
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from pets.models import Pet

from photos.models import Photo

from pets.forms import PetCreateForm, PetEditForm, PetDeleteForm, PetForm


class AddPetView(CreateView):
    model = Pet
    form_class = PetForm
    template_name = 'pets/add-pet-form.html'
    success_url = reverse_lazy('profile-details', kwargs={'pk': 1})

    def get_success_url(self):
        return reverse('accounts:details', kwargs={'pk': self.request.user.pk})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class PetDetailView(DetailView):
    model = Pet
    template_name = 'pets/pet-details-page.html'
    context_object_name = 'pet'
    slug_url_kwarg = 'pet_slug'

class EditPetView(UpdateView):
    model = Pet
    form_class = PetForm
    template_name = 'pets/edit-pet-page.html'
    slug_url_kwarg = 'pet_slug'
    context_object_name = 'pet'

    def get_success_url(self):
        return reverse_lazy('details', kwargs={'username': self.kwargs['username'], 'pet_slug': self.kwargs['pet_slug']})

class DeletePetView(DeleteView):
    model = Pet
    template_name = 'pets/delete-pet-page.html'
    context_object_name = 'pet'
    success_url = reverse_lazy('profile-details', kwargs={'pk': 1})

    def get_object(self, queryset=None):
        return Pet.objects.get(slug=self.kwargs['pet_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PetDeleteForm(initial=self.object.__dict__)
        return context

    def delete(self, request, *args, **kwargs):
        pet = self.get_object()
        pet.delete()
        return redirect(self.success_url)