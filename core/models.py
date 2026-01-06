from django.db import models
from datetime import date

class Trainer(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    contact_info = models.TextField(help_text="Dirección, Ciudad, etc.", blank=True)
    email = models.EmailField("Correo Electrónico", max_length=254, blank=True)
    phone = models.CharField("Teléfono / Celular", max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='trainers/', blank=True, null=True)

    @property
    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

class Client(models.Model):
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    # DATOS GENERALES
    full_name = models.CharField("Nombre Completo", max_length=200)
    birth_date = models.DateField("Fecha de nacimiento")
    gender = models.CharField("Género", max_length=10, choices=GENDER_CHOICES, default='M')
    city = models.CharField("Ciudad", max_length=100, blank=True)
    address = models.CharField("Dirección", max_length=255, blank=True)
    phone = models.CharField("Teléfono", max_length=20, blank=True)
    email = models.EmailField("Correo electrónico", blank=True)
    profile_picture = models.ImageField("Foto", upload_to='clients/', blank=True, null=True)
    
    # MOTIVACIÓN DEL USUARIO
    why_train = models.TextField("¿Por qué quiere entrenar?", blank=True)
    expectations = models.TextField("¿Qué espera lograr?", blank=True)
    fears = models.TextField("¿Qué le preocupa o le da miedo del ejercicio?", blank=True)
    process_explanation = models.TextField("Explicación del proceso de entrenamiento (entrenador)", blank=True)
    
    # CONTEXTO DEPORTIVO
    sport_practiced = models.CharField("Deporte practicado", max_length=100, blank=True)
    time_practicing = models.CharField("Tiempo de práctica", max_length=100, blank=True)
    stage = models.CharField("Etapa", max_length=50, choices=[
        ('Principiante', 'Principiante'),
        ('Intermedio', 'Intermedio'), 
        ('Semi-entrenado', 'Semi-entrenado'),
        ('Entrenado', 'Entrenado')
    ], blank=True)
    weekly_sessions = models.IntegerField("Sesiones semanales", default=0)
    sports_observations = models.TextField("Observaciones deportivas", blank=True)
    
    # OBJETIVOS
    main_goal = models.TextField("Objetivo principal", blank=True)
    secondary_goals = models.TextField("Objetivos secundarios", blank=True)
    trainer_goals = models.TextField("Objetivos del Entrenador", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

    @property
    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

class Measurement(models.Model):
    ACTIVITY_LEVEL_CHOICES = [
        ('1.2', 'Sedentario (poco o nada ejercicio)'),
        ('1.375', 'Ligera (1-3 días/sem)'),
        ('1.55', 'Moderada (3-5 días/sem)'),
        ('1.725', 'Intensa (6-7 días/sem)'),
        ('1.9', 'Muy Intensa (doble sesión)'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='measurements')
    date = models.DateField("Fecha de control", default=date.today)
    
    # DATOS ANTROPOMÉTRICOS AND GCT
    height = models.DecimalField("Talla (cm)", max_digits=5, decimal_places=2, help_text="Centímetros")
    weight = models.DecimalField("Peso (kg)", max_digits=5, decimal_places=2, help_text="Kg")
    imc = models.DecimalField("IMC", max_digits=5, decimal_places=2, blank=True, null=True)
    imc_category = models.CharField("Categoría IMC", max_length=100, blank=True)
    
    activity_level = models.CharField("Nivel de Actividad", max_length=10, choices=ACTIVITY_LEVEL_CHOICES, default='1.2')
    basal_metabolic_rate = models.DecimalField("Tasa Metabólica Basal (MB)", max_digits=6, decimal_places=0, blank=True, null=True, help_text="Kcal")
    total_caloric_expenditure = models.DecimalField("Gasto Calórico Total (GCT)", max_digits=6, decimal_places=0, blank=True, null=True, help_text="Kcal")

    fat_percentage = models.DecimalField("Porcentaje de grasa corporal (%)", max_digits=5, decimal_places=2, blank=True, null=True)
    colmen_fat_mass = models.DecimalField("Masa libre de grasa (kg)", max_digits=5, decimal_places=2, blank=True, null=True)
    obesity_type = models.CharField("Tipo de obesidad (Sí / No)", max_length=50, blank=True)
    anthropometry_observations = models.TextField("Observaciones Antropométricas", blank=True)

    # RM ESTIMADO
    rm_date = models.DateField("Fecha de control RM", blank=True, null=True)
    squat_weight = models.DecimalField("Sentadilla (Smith) (kg)", max_digits=6, decimal_places=2, blank=True, null=True)
    bench_press_weight = models.DecimalField("Press banca plano (kg)", max_digits=6, decimal_places=2, blank=True, null=True)
    hip_thrust_weight = models.DecimalField("Hip thrust (kg)", max_digits=6, decimal_places=2, blank=True, null=True)
    vertical_row_weight = models.DecimalField("Remo vertical (kg)", max_digits=6, decimal_places=2, blank=True, null=True)
    deadlift_weight = models.DecimalField("Peso muerto (kg)", max_digits=6, decimal_places=2, blank=True, null=True)

    # OBSERVACIONES GENERALES
    evaluations_done = models.TextField("Evaluaciones realizadas", blank=True, help_text="ej. FMS, pliegues cutáneos")
    additional_comments = models.TextField("Comentarios adicionales", blank=True)

    def __str__(self):
        return f"{self.client.full_name} - {self.date}"

    def save(self, *args, **kwargs):
        # Calculate IMC automatically
        if self.height and self.weight:
            # Convert height from cm to meters for BMI calculation
            height_m = float(self.height) / 100
            weight_kg = float(self.weight)
            self.imc = weight_kg / (height_m * height_m)
            
            # Basic IMC Category logic
            if self.imc < 18.5:
                self.imc_category = "Bajo peso"
            elif 18.5 <= self.imc < 24.9:
                self.imc_category = "Normal"
            elif 25 <= self.imc < 29.9:
                self.imc_category = "Sobrepeso"
            else:
                self.imc_category = "Obesidad"

            # Calculate MB (GCT Step 1)
            # Mifflin-St Jeor Formula
            # Men: (10 × weight) + (6.25 × height) − (5 × age) + 5
            # Women: (10 × weight) + (6.25 × height) − (5 × age) − 161
            
            age = self.client.age
            height_cm = float(self.height)
            
            mb = (10 * weight_kg) + (6.25 * height_cm) - (5 * age)
            
            if self.client.gender == 'M':
                mb += 5
            else:
                mb -= 161
            
            self.basal_metabolic_rate = mb
            
            # Calculate GCT (Step 2 & 3)
            activity_factor = float(self.activity_level)
            self.total_caloric_expenditure = mb * activity_factor

        super().save(*args, **kwargs)

class ClientImage(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='client_progress/')
    date = models.DateField(default=date.today)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Image for {self.client.full_name} on {self.date}"

class BusinessProfile(models.Model):
    description = models.TextField("Descripción de la empresa", help_text="Breve descripción para el pie de página")
    instagram_profile = models.URLField("Perfil de Instagram", blank=True)
    tiktok_profile = models.URLField("Perfil de TikTok", blank=True)
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and BusinessProfile.objects.exists():
            # If we're trying to save a new one but one exists, just update the existing one?
            # Or simpler: allow multiple but we only use the first one. Let's stick to simple models.
            pass 
        super().save(*args, **kwargs)

    def __str__(self):
        return "Perfil de la Empresa"
