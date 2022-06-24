from django.core.management.base import BaseCommand, CommandError
from ...models import Agency, Issue, Message, Question
import json

class Command(BaseCommand):
    help = 'Populates the DB with agencies, issues and questions'

    def handle(self, *args, **options):
        # Agency.objects.all().delete()
        Issue.objects.all().delete()
        Question.objects.all().delete()
        Message.objects.all().delete()
        # agencies = [("Nigeria Police Force", "NPF"), ("Lagos State Emergency Management Agency", "LASEMA")]
        # agency = [Agency(name=agent[0], acronym=agent[1]) for agent in agencies]
        # Agency.objects.bulk_create(agency)
        with open("/main/management/commands/output.json") as file:
            data = json.load(file)
        print(data.keys())
        for i in data.keys():
            print(i)
            data_ = data.get(i)
            # if data_ is None:
            #     continue
            # print(data_['description'])
            issue  =Issue.objects.create(name=data_["description"])
            questions = [Question(**i, issue=issue) for i in data_["flow"]]
            Question.objects.bulk_create(questions) 
            
        
           
        self.stdout.write(self.style.SUCCESS('Successfully added data'))