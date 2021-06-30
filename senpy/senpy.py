from .request_utils import post
from .user_token import get_token




def notify_me(content):
    """
    send a push notification with given content 

    parameters :
    content : text content of the push notification

    returns :
    """
    
    
    res = post('api/notif/notifyme', content, headers={"Authorization":get_token(), "Content-Type":"application/json"})
    if(res.status_code != 200):
            raise IOError("The message could not be sent")

    raise IOError("Failed to reached the server")