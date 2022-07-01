from rest_framework.exceptions import ValidationError

from main.models import Agency

def validate_responders(agencies):
    """Checks the list of agencies to see if there is any one that doesn't have a responder. If so, it raises an error.  """
    for agency in agencies:
        if agency.members.all().filter(role="escalator").exists():
            continue
        else:
            raise ValidationError(detail={
                "error": f"Cannot escalate because {agency.acronym} does not have an escalator account."
            })
    return True