from django.forms import model_to_dict
from django.test import TestCase
from .models import Report, AssignedCase
from main.models import Agency, Message
from django.contrib.auth import get_user_model
from faker import Faker

class TestReport(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        fake = Faker()
        agency = Agency.objects.create(name="Nigerian Police Force", acronym="NPF")
        test_user = User.objects.create(email="test@user.com",
                                        password="testpass123",
                                        first_name="John", 
                                        last_name="Doe", 
                                        phone="+2345960404544", 
                                        role="first_responder",
                                        is_active=True,
                                        agency=agency)
        message = Message.objects.create(name=fake.name(), category=fake.sentence(), issue=fake.text(), address=fake.address(), image_url1=fake.url())
        
        case = AssignedCase.objects.create(responder=test_user, case=message)
        Report.objects.create(assigned_case=case, situation_report=fake.text())
        Report.objects.create(assigned_case=case, situation_report=fake.text())
        Report.objects.create(assigned_case=case, situation_report=fake.text())
        Report.objects.create(assigned_case=case, situation_report=fake.text())
        
    def test_cases_assigned_delete(self):
        case = AssignedCase.objects.first()
        case.delete()
        
        self.assertEqual(False, case.is_active)
    
    def test_delete_corresponding_report(self):
        case = AssignedCase.objects.first()
        case.delete()
        reports = case.reports.all()
        
        self.assertEqual(False, case.is_active)
        for report in reports:
            self.assertEqual(False, report.is_active)
    
    def test_see_reports_from_message(self):
        message = Message.objects.first()
        # print(message.assigned.all().values())
        data = [{"first_responder": model_to_dict(case.responder,
                                                  exclude=['password',
                                                          'groups',
                                                          'user_permissions',
                                                          'agency',
                                                          'last_login']),
                 "agency":model_to_dict(case.responder.agency),
                 "escalator_note": case.escalator_note, 
                 "status":case.status, 
                 'reports':case.report_detail 
                 } for case in message.assigned.all()]
        
        print(data)
        
        