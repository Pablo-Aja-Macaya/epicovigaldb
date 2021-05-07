from django.db import models
import datetime

# Modelos

class Report(models.Model):
    OPCIONES_TIPO = (
        ('privado','privado'),
        ('mensual','mensual'),
        ('general','general')
    )
    OPCIONES_CATEGORIA = (
        ('vigilancia','vigilancia'),
        ('aleatoria','aleatoria'),
        ('no aleatoria','no aleatoria'),
    )

    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=20, default=None, blank=True)
    subtitulo = models.TextField(max_length=50, default=None)

    tipo = models.CharField(max_length=10, default='mensual', choices=OPCIONES_TIPO)
    categoria = models.CharField(max_length=20, default='vigilancia', choices=OPCIONES_CATEGORIA)
    umbral = models.IntegerField(default=None, blank=True, null=True)
    
    fecha_inicial = models.DateField(default='2020-01-01')
    fecha_final = models.DateField(default='2020-01-30')
    fecha_publ = models.DateTimeField(auto_now=True)

    texto_informacion = models.TextField(max_length=600, default=None, blank=True)
    texto_procedencia = models.TextField(max_length=600, default=None, blank=True)
    texto_variantes_hospitales = models.TextField(max_length=600, default=None, blank=True)
    texto_variantes_galicia = models.TextField(max_length=600, default=None, blank=True)
    texto_geolocalizacion_concellos = models.TextField(max_length=600, default=None, blank=True)
    texto_variantes_lineas = models.TextField(max_length=600, default=None, blank=True)
    texto_variantes_columnas = models.TextField(max_length=600, default=None, blank=True)

    def days_since_pub(self):
        actual = datetime.date.today()
        pub = datetime.datetime.strptime(str(self.fecha_publ).split(' ')[0], "%Y-%m-%d").date()
        dias = (actual-pub).days
        if dias==0:
            return 'Publicado hoy'
        elif dias>0:
            return f'Hace {dias} días' 
    def get_month(self):
        m = datetime.datetime.strptime(str(self.fecha_inicial), "%Y-%m-%d").strftime("%B")
        meses = {
            'January':'Enero',
            'February':'Febrero',
            'March':'Marzo',
            'April':'Abril',
            'May':'Mayo',
            'June':'Junio',
            'July':'Julio',
            'August':'Agosto',
            'September':'Septiembre',
            'October':'Octubre',
            'November':'Noviembre',
            'December':'Diciembre', 
        }
        m = meses[m]
        return m
    def get_date_español(self):
        m1 = datetime.datetime.strptime(str(self.fecha_inicial), "%Y-%m-%d").strftime("%B")
        m2 = datetime.datetime.strptime(str(self.fecha_final), "%Y-%m-%d").strftime("%B")

        d1 = datetime.datetime.strptime(str(self.fecha_inicial), "%Y-%m-%d").strftime("%A")
        d2 = datetime.datetime.strptime(str(self.fecha_final), "%Y-%m-%d").strftime("%A")
        d1_n = datetime.datetime.strptime(str(self.fecha_inicial), "%Y-%m-%d").strftime("%d")
        d2_n = datetime.datetime.strptime(str(self.fecha_final), "%Y-%m-%d").strftime("%d")
        y1 = datetime.datetime.strptime(str(self.fecha_inicial), "%Y-%m-%d").year
        y2 = datetime.datetime.strptime(str(self.fecha_final), "%Y-%m-%d").year
        meses = {
            'January':'Enero',
            'February':'Febrero',
            'March':'Marzo',
            'April':'Abril',
            'May':'Mayo',
            'June':'Junio',
            'July':'Julio',
            'August':'Agosto',
            'September':'Septiembre',
            'October':'Octubre',
            'November':'Noviembre',
            'December':'Diciembre', 
        }
        dias = {
            'Monday':'Lunes',
            'Tuesday':'Martes',
            'Wednesday':'Miércoles',
            'Thursday':'Jueves',
            'Friday':'Viernes',
            'Saturday':'Sábado',
            'Sunday':'Domingo'
        }
        m1 = meses[m1]
        m2 = meses[m2]
        d1 = dias[d1]
        d2 = dias[d2]

        fecha_i = f'{d1}, {d1_n} de {m1}, {y1}'
        fecha_f = f'{d2}, {d2_n} de {m2}, {y2}'

        fecha = fecha_i + ' - ' + fecha_f

        return fecha

    def get_year(self):
        y = datetime.datetime.strptime(str(self.fecha_inicial), "%Y-%m-%d").year
        return y
    def __str__(self):
        return f'{str(self.id)} - {str(self.titulo)} - {str(self.categoria)}'
