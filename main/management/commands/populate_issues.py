from django.core.management.base import BaseCommand, CommandError
from ...models import Agency, Issue, Message, Question
import json

class Command(BaseCommand):
    help = 'Populates the DB with agencies, issues and questions'

    def handle(self, *args, **options):
        Issue.objects.all().delete()
        Question.objects.all().delete()
        
        
        data =  {
  "1": {
    "description": "Rape",
    "flow": [
      {
        "question": "Describe details of the incident"
      },
      {
        "question": "Has the victim (he/she) had a bath?"
      },
      {
        "question": "Has the victim reported to any police station?"
      },
      {
        "question": "What is the name of the victim?"
      },
      {
        "question": "What is the gender of the victim?"
      }
    ]
  },
  "2": {
    "description": "Child Abuse",
    "flow": [
      {
        "question": "Describe details of the incident"
      },
      {
        "question": "Send us a picture or # to cancel this operation"
      },
      {
        "question": "Please, is the child in immediate danger?"
      },
      {
        "question": "Is the child injured? if yes, what is the type of injury? "
      },
      {
        "question": "What is the name of the victim?"
      },
      {
        "question": "What is the gender of the victim?"
      }
    ]
  },
  "3": {
    "description": "Domestic Violence",
    "flow": [
      {
        "question": "Describe details of the incident"
      },
      {
        "question": "Send us a picture",
        "is_image" : True
      },
      {
        "question": "What is the victim's location?"
      },
      {
        "question": "Do you know the culprit?"
      },
      {
        "question": "Are you in immediate danger as we speak?"
      },
      {
        "question": "What is the name of the victim?"
      },
      {
        "question": "What is the gender of the victim?"
      }
    ]
  },
  "4": {
    "description": "Complaints",
    "flow": [
      {
        "question": "Kindly confirm number used to call in with?"
      },
      {
        "question": "What is your complaint?"
      }
      
    ]
  },
  "5": {
    "description": "Missing Person",
    "flow": [
      {
        "question": "What is the name of the victim?"
      },
      {
        "question": "What is the gender of the victim?"
      },
      {
        "question": "How old is the victim?"
      },
      {
        "question": "Tell us the Home address/Family address of the victim"
      },
      {
        "question": "Send us a picture of the missing person",
        "is_image" : True
      }
    ]
  },
  "6": {
    "description": "Dead Body",
    "flow": [
      {
        "question": "Describe details of the incident"
      },
      {
        "question": "Send us a picture",
        "is_image" : True
      }
    ]
  },
  "7": {
    "description": "Collapsed Building",
    "flow": [
      {
        "question": "Incident location details( Street name & number, Landmark/bus stop Area/Location/ l.ga.)"
      },
      {
        "question": "Send us a picture",
        "is_image" : True
      },
      {
        "question": "Are there any casualities?"
      },
      {
        "question": "Is anyone trapped in the structure/building?"
      }
    ]
  },
  "8": {
    "description": "Accident",
    "flow": [
      {
        "question": "Describe details of the incident"
      },
      {
        "question": "Send us a picture",
        "is_image" : True
      },
      {
        "question": "Are there any casualities?"
      },
      {
        "question": "Is anyone trapped in the structure/building/vehicle?"
      },
      {
        "question": "Is there a fuel leak/smoke?"
      }
    ]
  },
  "9": {
    "description": "Fight",
    "requiresImg": True,
    "flow": [
      {
        "question": "Describe details of the incident"
      },
      {
        "question": "Are there any casualities?"
      },
      {
        "question": "Send us a picture",
        "is_image" : True
      }
    ]
  },
  "10": {
    "description": "Fire Outbreak",
    "flow": [
      {
        "question": "Describe details of the incident"
      },
      {
        "question": "Send us a picture",
        "is_image" : True
      },
      {
        "question": "Are there any casualities?"
      },
      {
        "question": "Is it a bungalow or storey building?"
      },
      {
        "question": "Is anyone trapped in the structure/building?"
      }
    ]
  },
  "11": {
    "description": "Robbery (Traffic/Vehicle)",
    "requiresImg": True,
    "flow": [
      {
        "question": "Describe details of the incident"
      },
      {
        "question": "Location of the incident?"
      },
      {
        "question": "Send us a picture",
        "is_image" : True
      },
      {
        "question": "Are there any casualities?"
      }
    ]
  },
  "12": {
    "description": "Plane Crash",
    "flow": [
      {
        "question": "Describe details of the incident"
      },
      {
        "question": "Location of the incident?"
      },
      {
        "question": "Send us a picture",
        "is_image" : True
      }
    ]
  },
  "13": {
    "description": "Suspicious Person Movement",
    "flow": [
      {
        "question": "What makes this person/movement suspicious?"
      },
      {
        "question": "How long has this incident been going on?"
      },
      {
        "question": "How many are they in number?"
      },
      {
        "question": "How are they dressed?"
      },
      {
        "question": "Give us a Location of the incident?"
      },
      {
        "question": "Send us a picture",
        "is_image" : True
      }
    ]
  },
  "14": {
    "description": "Destitute and Abandoned Baby",
    "flow": [
      {
        "question": "Describe the details of the emergency"
      },
      {
        "question": "Give us a Location of the incident?"
      },
      {
        "question": "Send us a picture",
        "is_image" : True
      }
    ]
  }
}
        
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