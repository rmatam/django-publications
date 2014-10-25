# -*- coding: utf-8 -*-

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import transaction
from publications.models import Publication, Type

class Tests(TestCase):
	fixtures = ['initial_data.json', 'test_data.json']
	urls = 'publications.tests.urls'

	def setUp(self):
		User.objects.create_superuser('admin', 'admin@test.de', 'admin')


	def test_authors(self):
		publication = Publication.objects.create(
			type=Type.objects.get(pk=1),
			authors=u'Jörn-Philipp Lies and Ralf M. Häfner and M. Bethge',
			title=u'Slowness and sparseness have diverging effects on complex cell learning',
			year=2014,
			journal=u'PLoS Computational Biology',
			external=0)
		publication.save()

		self.assertEqual(len(publication.authors_list), 3)
		self.assertEqual(publication.authors_list[0], 'J.-P. Lies')


	def test_publications(self):
		self.assertEqual(self.client.get('/publications/').status_code, 200)


	def test_bibtex_import(self):
		self.client.login(username='admin', password='admin')

		count = Publication.objects.count()
		response = self.client.post('/admin/publications/publication/import_bibtex/',
			{'bibliography': TEST_BIBLIOGRAPHY}, follow=False)

		self.assertEqual(Publication.objects.count() - count, TEST_BIBLIOGRAPHY_COUNT)


TEST_BIBLIOGRAPHY_COUNT = 4
TEST_BIBLIOGRAPHY = r"""
@article{Bethge2002c,
  author = "M. Bethge and D. Rotermund and K. Pawelzik",
  title = "Optimal short-term population coding: when Fisher information fails",
  year = 2002,
  journal = "Neural Computation",
  month = "Oct",
  keywords = "population coding, fisher information",
  doi = "10.1162/08997660260293247",
  url = "http://www.mitpressjournals.org/doi/abs/10.1162/08997660260293247"
}

@article{Simovski2011,
  author =        {Simovski, Constantin R.},
  journal =       {J. Opt.},
  month =         jan,
  number =        {1},
  pages =         {013001},
  title =         {{On electromagnetic characterization and
                   homogenization of nanostructured metamaterials}},
  volume =        {13},
  year =          {2011},
  doi =           {10.1088/2040-8978/13/1/013001},
  issn =          {2040-8978},
  url =           {http://stacks.iop.org/2040-8986/13/i=1/
                  a=013001?key=crossref.7321766a6630b917c6f066f2abc1e2cc},
}

@inproceedings{gerwinn2008bayesian,
  title={Bayesian inference for spiking neuron models with a sparsity prior},
  author={Gerwinn, Sebastian and Macke, Jakob and Seeger, Matthias and Bethge, Matthias},
  booktitle={Proceedings of the 21st Annual Conference on Neural Information Processing Systems},
  number={EPFL-CONF-161311},
  pages={529--536},
  year={2008}
}

@article{hafner2000dynamical,
  title={A dynamical model of the inner Galaxy},
  author={H{\"a}fner, Ralf and Evans, N Wyn and Dehnen, Walter and Binney, James},
  journal={Monthly Notices of the Royal Astronomical Society},
  volume={314},
  number={3},
  pages={433--452},
  year={2000},
  publisher={Oxford University Press}
}
"""
