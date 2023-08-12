from logs.models import LogAuthUser, LogsInvites, LogTasks
from ..models import User
def create_log_auth(request, text:str, user=None):

    """
    Create log of auth \n
    request:: user request \n
    text : str :: text of message log
    """
    if not user:
        user = request.user

    log_auth = LogAuthUser.objects.create(
                    user=user,
                    do=text
                )
    
    if request.user.is_authenticated :
        log_auth.company = request.user.corporation
    
    log_auth.save()


def create_log_invite(request, text:str, code:str,
                      creator=None):
    
    if not creator:
        creator = request.user

    log = LogsInvites.objects.create(
            company= User.objects.get(username=request.user.username).corporation,
            code=code,
            do=text,
            creator=creator
            
        )
    
    
    log.save()


def create_log_tasks(request, text):
    log = LogTasks(
                company=request.user.corporation,
                user=request.user,
                do=text
                )
    log.save()

