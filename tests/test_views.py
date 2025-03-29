from django.test import TestCase
from django.urls import reverse

class PageAccessTest(TestCase):
	def setUp(self):
		# Define all the pages you want to test (URL names from urls.py)
		self.pages = [

			{"name": "home", "args": []},
<<<<<<< HEAD
=======
			{"name": "materials:subjects-list", "args": []},
			{"name": "problems", "args": []},
			{"name": "about", "args": []},
			{"name": "donate", "args": []},
			{"name": "users:login", "args": []},
			{"name": "users:register", "args": []},
>>>>>>> 1537deb4fa5435b70984fb9cf315a63e6ea3f8b3

		]

	def test_pages_are_accessible(self):
		"""Test if all specified pages return status code:200 (OK)"""
		for page in self.pages:
			url = reverse(page["name"], args=page["args"])
			response = self.client.get(url)
			self.assertEqual(response.status_code, 200, f"Page {page['name']} failed to load!")

