

## Test
from django.test.utils import setup_test_environment
setup_test_environment()

from django.test import Client
client = Client()

from django.core.urlresolvers import reverse

from polls.models import Question
from django.utils import timezone