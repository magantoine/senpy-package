from .request_utils import post, handle_request_error

def notify_me(content="New notification!"):
    """
    send a push notification with given content 

    parameters :
    content : text content of the push notification

    returns :
    """
    res = post('notif/notifyme', 
                json={"message": content})
    if 'python_error' in res or res.status_code != 200:
        handle_request_error(res)

