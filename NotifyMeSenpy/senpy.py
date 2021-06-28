from request_utils import post
import user_token




def notify_me(content, tries=200):
    """
    send a push notification with given content 

    parameters :
    content : text content of the push notification

    returns :
    """
    
    success = False
    while(not success and tries > 0):
        res = post('api/job/notifyme', content, headers={"token":user_token.get_token()})
        if(res.status_code != 200):
            tries -= 1

    raise IOError("Failed to reached the server")