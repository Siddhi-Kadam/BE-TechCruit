from import_export import resources
from .models import TestQuestions


class ImportsResource(resources.ModelResource):
    class meta:
        model = TestQuestions