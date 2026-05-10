from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import Client, Measurement, Trainer, ClientImage, BusinessProfile, Profile, Role, TrainingSession
from .forms import ClientForm, MeasurementForm, TrainerForm, ClientImageForm, BusinessProfileForm
from datetime import datetime, timedelta, time, date
class BusinessProfileUpdateView(UpdateView):
    model = BusinessProfile
    form_class = BusinessProfileForm
    template_name = 'core/business_profile_form.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        # Get the first one or create it if it doesn't exist
        obj, created = BusinessProfile.objects.get_or_create(defaults={'description': 'Bienvenido a Training Home.'})
        return obj

from django.views import View

class HomeView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Redirigir al login si no está autenticado
            return redirect('login')
            
        # Si es superusuario de Django, mostrar dashboard admin
        if request.user.is_superuser:
            return self.render_admin_dashboard(request)
            
        # Validar el rol del perfil
        if hasattr(request.user, 'perfil_app') and request.user.perfil_app.rol:
            rol = request.user.perfil_app.rol.nombre_rol.lower()
            if 'admin' in rol:
                return self.render_admin_dashboard(request)
            elif 'entrenador' in rol:
                return redirect('trainer_agenda')
            elif 'cliente' in rol:
                cliente_rel = request.user.perfil_app.clientes.first()
                if cliente_rel:
                    return redirect('client_detail', pk=cliente_rel.pk)
                else:
                    return redirect('client_booking')
                    
        # Fallback si no tiene rol o es desconocido
        return self.render_admin_dashboard(request)

    def render_admin_dashboard(self, request):
        context = {}
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
            
        return render(request, 'core/home.html', context)

class ClientListView(ListView):
    model = Client
    template_name = 'core/client_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        qs = Client.objects.filter(is_active=True)
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(full_name__icontains=query)
        return qs

class ClientArchiveListView(ListView):
    model = Client
    template_name = 'core/client_archive_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        qs = Client.objects.filter(is_active=False)
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(full_name__icontains=query)
        return qs

from django.http import HttpResponseRedirect

def client_archive_toggle(request, pk):
    client = get_object_or_404(Client, pk=pk)
    client.is_active = not client.is_active
    client.save()
    if client.is_active:
        return HttpResponseRedirect(reverse_lazy('client_list'))
    else:
        return HttpResponseRedirect(reverse_lazy('client_archive_list'))

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

    def form_valid(self, form):
        if hasattr(self.request.user, 'perfil_app'):
            trainer = self.request.user.perfil_app.trainers.first()
            if trainer:
                form.instance.entrenador_asignado = trainer
        return super().form_valid(form)

class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'core/client_form.html'
    
    def get_success_url(self):
        return reverse_lazy('client_detail', kwargs={'pk': self.object.pk})

class ClientDeleteView(View):
    def get(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        return render(request, 'core/client_confirm_delete.html', {'object': client})

    def post(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        client.is_active = False
        client.save()
        return redirect('client_list')

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
        is_admin = False
        context['trainer'] = None

        if self.request.user.is_authenticated and hasattr(self.request.user, 'perfil_app'):
            rol = self.request.user.perfil_app.rol.nombre_rol.lower()

            if 'admin' in rol:
                is_admin = True
            elif 'cliente' in rol:
                cliente = self.request.user.perfil_app.clientes.first()
                if cliente:
                    context['trainer'] = cliente.entrenador_asignado
            elif 'entrenador' in rol:
                context['trainer'] = self.request.user.perfil_app.trainers.first()

        if getattr(self.request.user, 'is_superuser', False):
            is_admin = True

        if is_admin:
            context['trainers_list'] = Trainer.objects.all().prefetch_related('clientes_asignados')
            context['total_clients'] = Client.objects.filter(is_active=True).count()
            context['is_admin_view'] = True
        elif not context['trainer']:
            context['trainer'] = Trainer.objects.first()

        return context

class TrainerCreateView(CreateView):
    model = Trainer
    form_class = TrainerForm
    template_name = 'core/trainer_form.html'
    success_url = reverse_lazy('trainer_detail')

    def dispatch(self, request, *args, **kwargs):
        # Specific check: if a trainer already exists, redirect to detail
        if Trainer.objects.exists() and not request.user.is_superuser:
            return redirect('trainer_detail')
        return super().dispatch(request, *args, **kwargs)

class TrainerUpdateView(UpdateView):
    model = Trainer
    form_class = TrainerForm
    template_name = 'core/trainer_form.html'
    success_url = reverse_lazy('trainer_detail')

    def get_object(self):
        if self.request.user.is_authenticated and hasattr(self.request.user, 'perfil_app'):
            trainer = self.request.user.perfil_app.trainers.first()
            if trainer: return trainer
        return Trainer.objects.first()

class TrainerDeleteView(DeleteView):
    model = Trainer
    template_name = 'core/trainer_confirm_delete.html'
    success_url = reverse_lazy('trainer_detail')

    def get_object(self):
        if self.request.user.is_authenticated and hasattr(self.request.user, 'perfil_app'):
            trainer = self.request.user.perfil_app.trainers.first()
            if trainer: return trainer
        return Trainer.objects.first()

# ===============================================
# VISTAS DE AGENDA
# ===============================================

class TrainerAgendaView(TemplateView):
    template_name = 'core/agenda_entrenador.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.request.user, 'perfil_app'):
            trainer = self.request.user.perfil_app.trainers.first()
            if trainer:
                sesiones = TrainingSession.objects.filter(entrenador=trainer).order_by('fecha_hora')
                context['sesiones'] = sesiones
        return context


class ClientBookingView(TemplateView):
    template_name = 'core/agenda_cliente.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        horas_disponibles = []
        fecha_str = self.request.GET.get('fecha')
        
        if not fecha_str:
             fecha = date.today() + timedelta(days=1)
        else:
             fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
             
        context['fecha_seleccionada'] = fecha
        
        if hasattr(self.request.user, 'perfil_app'):
             client = self.request.user.perfil_app.clientes.first()
             if client:
                  context['mis_sesiones'] = TrainingSession.objects.filter(cliente=client).order_by('-fecha_hora')
                  if client.entrenador_asignado:
                      entrenador = client.entrenador_asignado
                      
                      start_of_day = datetime.combine(fecha, time.min)
                      end_of_day = datetime.combine(fecha, time.max)
                      sesiones_ocupadas = TrainingSession.objects.filter(
                          entrenador=entrenador,
                          fecha_hora__range=(start_of_day, end_of_day),
                          estado__in=['Pendiente', 'Realizado']
                      ).values_list('fecha_hora', flat=True)
                      
                      horas_ocupadas_str = [s.strftime('%H:%M') for s in sesiones_ocupadas]
                      
                      hora_inicio = 8
                      hora_fin = 20
                      for h in range(hora_inicio, hora_fin):
                          hora_str = f"{h:02d}:00"
                          if hora_str not in horas_ocupadas_str:
                              horas_disponibles.append(hora_str)
                      
                      context['horas_disponibles'] = horas_disponibles
                      context['entrenador'] = entrenador
        return context

    def post(self, request, *args, **kwargs):
        fecha_str = request.POST.get('fecha')
        hora_str = request.POST.get('hora')
        
        if hasattr(request.user, 'perfil_app'):
             client = request.user.perfil_app.clientes.first()
             if client and client.entrenador_asignado:
                  fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
                  hora_parts = hora_str.split(':')
                  dt = datetime.combine(fecha, time(int(hora_parts[0]), int(hora_parts[1])))
                  
                  if not TrainingSession.objects.filter(entrenador=client.entrenador_asignado, fecha_hora=dt, estado__in=['Pendiente', 'Realizado']).exists():
                      TrainingSession.objects.create(
                          cliente=client,
                          entrenador=client.entrenador_asignado,
                          fecha_hora=dt,
                          estado='Pendiente'
                      )
        return redirect('client_booking')

