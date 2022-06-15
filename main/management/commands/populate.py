from django.core.management.base import BaseCommand, CommandError
from ...models import Agency, Issue, Question


class Command(BaseCommand):
    help = 'Populates the DB with agencies, issues and questions'

    def handle(self, *args, **options):
        Agency.objects.delete()
        Issue.objects.delete()
        Question.objects.delete()
        agencies = [("Nigeria Police Force", "NPF"), ("Lagos State Emergency Management Agency", "LASEMA")]
        agency = [Agency(name=agent[0], acronym=agent[1]) for agent in agencies]
        Agency.objects.bulk_create(agency)
        
        issues = ["Fight", "Rape", "Dead Body"]
        
        Issue.objects.bulk_create([Issue(name=issue) for issue in issues])
        
        questions = {
            issues[0] : ["Describe the details of the incident", "Please send us a picture."],
            issues[1] : ['Describe details of the incident', 
                         'What is the victim name?', 
                         'How old is he/she?', 
                         'What is the victim\'s gender?', 
                         'Have the victim (he/she) had a bath?', 
                         'Have the victim reported to any police station?' ],
            issues[3] : ["Describe the details of the incident", "Please send us a picture."],
        }
        
        
        for issue in issues:
            ish = Issue.objects.get(name = issue)
            Question.objects.bulk_create([Question.objects.create(issue=ish,question = question) for question in questions[issue]])
            
        self.stdout.write(self.style.SUCCESS('Successfully added data'))