from django.test import TestCase
from django.urls import reverse
from authentication.models import User
from .models import Patient
from diagnostico.models import AIDiagnosis
from datetime import date

class DiagnosisHistoryTests(TestCase):
	def setUp(self):
		# Crear usuario médico radiólogo
		self.user = User.objects.create_user(
			email='doc@example.com',
			password='testpassword',
			first_name='Doctor',
			last_name='Tester',
			identificacion='DOC123',
			rol='MEDICO_RADIOLOGO'
		)

		# Crear paciente
		self.patient = Patient.objects.create(
			identification='P1001',
			first_name='Paciente',
			last_name='Ejemplo',
			date_of_birth=date(1980, 1, 1),
			gender='M',
			created_by=self.user,
			is_active=True,
		)

		# Crear diagnósticos
		AIDiagnosis.objects.create(patient=self.patient, requested_by=self.user, status='COMPLETED', diagnosis_result='Resultado A')
		AIDiagnosis.objects.create(patient=self.patient, requested_by=self.user, status='COMPLETED', diagnosis_result='Resultado B')

	def test_dashboard_shows_historial_button(self):
		self.client.force_login(self.user)
		url = reverse('users:user_dashboard')
		response = self.client.get(url)
		self.assertContains(response, 'Historial de Diagnósticos')

	def test_diagnosis_history_view_displays_diagnoses(self):
		self.client.force_login(self.user)
		url = reverse('users:diagnosis_history') + f'?patient_id={self.patient.id}'
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		# Should list the diagnoses
		self.assertContains(response, 'Diagnósticos (')
		self.assertContains(response, 'Resultado A')
		self.assertContains(response, 'Resultado B')

	def test_diagnosis_history_restricted_for_technician(self):
		# Create a technician user
		tech_user = User.objects.create_user(
			email='tech@example.com',
			password='testpassword',
			first_name='Tech',
			last_name='User',
			identificacion='TECH1',
			rol='TECNICO_SALUD'
		)
		self.client.force_login(tech_user)
		url = reverse('users:diagnosis_history')
		response = self.client.get(url)
		# Should redirect to dashboard since permission denied
		self.assertEqual(response.status_code, 302)
# Create your tests here.
