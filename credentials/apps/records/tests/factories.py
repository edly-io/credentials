import factory
from factory.fuzzy import FuzzyChoice, FuzzyDecimal

from credentials.apps.catalog.tests.factories import CourseRunFactory
from credentials.apps.core.tests.factories import UserFactory
from credentials.apps.credentials.tests.factories import ProgramCertificateFactory
from credentials.apps.records import models


class UserGradeFactory(factory.django.DjangoModelFactory):
    class Meta(object):
        model = models.UserGrade

    username = factory.Sequence(lambda o: 'robot%d' % o)
    course_run = factory.SubFactory(CourseRunFactory)
    letter_grade = FuzzyChoice(['A', 'B', 'C', 'D', 'F'])
    percent_grade = FuzzyDecimal(0.0, 1.0, precision=4)
    verified = True


class ProgramCertRecordFactory(factory.django.DjangoModelFactory):
    class Meta(object):
        model = models.ProgramCertRecord

    certificate = factory.SubFactory(ProgramCertificateFactory)
    user = factory.SubFactory(UserFactory)