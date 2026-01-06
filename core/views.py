from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView, DeleteView
from django.urls import reverse_lazy
from .models import Client, Measurement, Trainer, ClientImage, BusinessProfile
from .forms import ClientForm, MeasurementForm, TrainerForm, ClientImageForm, BusinessProfileForm

class BusinessProfileUpdateView(UpdateView):
    model = BusinessProfile
    form_class = BusinessProfileForm
    template_name = 'core/business_profile_form.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        # Get the first one or create it if it doesn't exist
        obj, created = BusinessProfile.objects.get_or_create(defaults={'description': 'Bienvenido a Training Home.'})
        return obj

class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clients'] = Client.objects.all().order_by('-created_at')[:5]
        context['trainer'] = Trainer.objects.first()
        
        if context['trainer'] and context['trainer'].bio:
            bio = context['trainer'].bio
            words = bio.split()
            if len(words) > 20:
                context['short_bio'] = " ".join(words[:20]) + "..."
            else:
                context['short_bio'] = bio
        else:
            context['short_bio'] = ""

        return context

class ClientListView(ListView):
    model = Client
    template_name = 'core/client_list.html'
    context_object_name = 'clients'

class ClientDetailView(DetailView):
    model = Client
    template_name = 'core/client_detail.html'
    context_object_name = 'client'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get measurements specific to this client
        measurements = self.object.measurements.all().order_by('date')
        context['measurements'] = measurements
        
        # Prepare data for charts/comparison if needed
        if measurements.exists():
            context['initial_measurement'] = measurements.first()
            latest = measurements.last()
            context['latest_measurement'] = latest
            
            # Formatted values for template
            context['gct_display'] = latest.total_caloric_expenditure if latest.total_caloric_expenditure else "--"
            context['tmb_display'] = latest.basal_metabolic_rate if latest.basal_metabolic_rate else "--"
            
        context['images'] = self.object.images.all().order_by('-date')
        return context

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'core/client_form.html'
    success_url = reverse_lazy('client_list')

class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'core/client_form.html'
    
    def get_success_url(self):
        return reverse_lazy('client_detail', kwargs={'pk': self.object.pk})

class MeasurementCreateView(CreateView):
    model = Measurement
    form_class = MeasurementForm
    template_name = 'core/measurement_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client_id = self.kwargs.get('client_id')
        if client_id:
            context['client'] = get_object_or_404(Client, pk=client_id)
        return context

    def form_valid(self, form):
        client_id = self.kwargs.get('client_id')
        form.instance.client = get_object_or_404(Client, pk=client_id)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('client_detail', kwargs={'pk': self.object.client.pk})

class ClientImageCreateView(CreateView):
    model = ClientImage
    form_class = ClientImageForm
    template_name = 'core/image_form.html'
    
    def form_valid(self, form):
        client_id = self.kwargs.get('client_id')
        form.instance.client = get_object_or_404(Client, pk=client_id)
        return super().form_valid(form)
        
    def get_success_url(self):
        return reverse_lazy('client_detail', kwargs={'pk': self.object.client.pk})

class TrainerDetailView(TemplateView):
    template_name = 'core/trainer_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trainer'] = Trainer.objects.first()
        return context

class TrainerCreateView(CreateView):
    model = Trainer
    form_class = TrainerForm
    template_name = 'core/trainer_form.html'
    success_url = reverse_lazy('trainer_detail')

    def dispatch(self, request, *args, **kwargs):
        # Specific check: if a trainer already exists, redirect to detail
        if Trainer.objects.exists():
            return redirect('trainer_detail')
        return super().dispatch(request, *args, **kwargs)

class TrainerUpdateView(UpdateView):
    model = Trainer
    form_class = TrainerForm
    template_name = 'core/trainer_form.html'
    success_url = reverse_lazy('trainer_detail')

    def get_object(self):
        return Trainer.objects.first()

class TrainerDeleteView(DeleteView):
    model = Trainer
    template_name = 'core/trainer_confirm_delete.html'
    success_url = reverse_lazy('trainer_detail')

    def get_object(self):
        return Trainer.objects.first()

