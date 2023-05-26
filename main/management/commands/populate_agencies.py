from django.core.management.base import BaseCommand, CommandError
from ...models import Agency, EmergencyCode
import json
import re
import csv

class Command(BaseCommand):
    help = 'Populates the DB with agencies, issues and questions'

    def handle(self, *args, **options):
        Agency.objects.all().delete()
        EmergencyCode.objects.all().delete()
        
        
        # agencies = """LASEMA ,RRS,LASEMA,MINISTRY OF JUSTICE,LASEMA ,RRS,LASEMA , RRS,LASEMA, RRS,LASEMA ,RRS,LASEMA,RRS,LASEMA, RRS,LASEMA ,RRS,LASEMA ,RRS,LASEMA ,RRS,LASEMA ,RRS,LASEMA,RRS,LASEMA,LASEMA,LASAMBUS,LASEMA , LASAMBUS, LASEMA, LASTMA, LASEMA,LASEMA, LASTMA,LASEMA ,RRS,LASEMA ,LASTMA,LASEMA,LASEMA,LASEMA ,RRS,LASEMA ,RRS,LASEMA ,RRS,LASEMA,RRS,LASEMA , RRS,LASEMA ,RRS,LASEMA,RRS,LASEMA ,RRS,LASEMA RRS,LASEMA,LASEMA,LASEPA ,LASEMA, LASAMBUS,RRS,FIRE SERVICE,LASEMA ,FIRE SERVICE,LASEMA,LASEMA, LASAMBUS,RRS,FIRE SERVICE,LASEMA, LASAMBUS,RRS,FIRE SERVICE,LASEMA, LASAMBUS,RRS,FIRE SERVICE,LASEMA, RRS ,LASEMA, RRS, LASEMA,LASEMA,LASAMBUS,LASEMA, WAPA, OFFICE OF YOUTH AND SOCIAL DEVELOPMENT, SOCIAL WELFARE,LASEMA ,RRS,LASEMA , RRS,LASEMA, SEHMU,RRS,LASEMA , RRS,LASEMA , RRS,LASEMA,LASEMA, RRS, LASAMBUS, FIRE SERVICE, LASTMA,LASEMA, RRS, LASAMBUS, FIRE SERVICE, LASTMA,LASEMA,LASEMA ,RRS,LASEMA ,RRS,LASEMA ,RRS,LASEMA ,RRS,LASEMA , RRS,LASEMA,LASEMA ,RRS,LASEMA ,RRS,LASEMA ,RRS,LASEMA ,LASEMA ,LASEMA ,LASEMA,LASEMA,LASEMA,LASEMA,LASEMA""".split(",")
        # print(set(agencies))
        
        agencies = {'LASEPA', 'FIRE SERVICE', 'FIRE SERVICE', 'OFFICE OF YOUTH AND SOCIAL DEVELOPMENT', 'LASTMA', 'LASTMA', 'MINISTRY OF JUSTICE', 'RRS', ' WAPA', 'RRS', 'LASAMBUS', 'LASAMBUS', 'LASEMA', 'SEHMU', 'LASEMA', 'LASEMA', 'SOCIAL WELFARE', 'RRS'}
        
        agency_list = []
        for agency_name in set(agencies):
            print(agency_name.strip().rstrip(), "\n")
            
            agency_list.append(Agency(acronym=agency_name.strip().rstrip()))
            
        Agency.objects.bulk_create(agency_list)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully added {len(agency_list)} agencies'))
        
        self.stdout.write(self.style.NOTICE(f'Creating codes'))
        
        
        
        
        with open('codes.csv', "r") as file:
            csv_file = csv.DictReader(file)
            Codes = []
            for row in csv_file:
                print(row, "\n")
                
                responders = list(map(lambda x: Agency.objects.get(acronym=x.strip().rstrip()).id, row['responders'].split(",")))
                code = row['\ufeffcode'] + " - " + row['incident']
                # code = row['code'] + " - " + row['incident']
                
                
                
                emergency = EmergencyCode(code=code)
                emergency.save()
                emergency.agency.add(*responders)
                Codes.append(emergency)
                
            
        self.stdout.write(self.style.SUCCESS(f'Successfully added {len(Codes)} emergency codes'))