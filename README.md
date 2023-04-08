## Installing

```shell
git clone https://github.com/hikehikehike/izi_simple_chat
cd izi_simple_chat
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
## Usage
1. http://127.0.0.1:8000/api/user/register/ (Register)
2. http://127.0.0.1:8000/api/user/token/  (Take access and refresh token)
3. http://127.0.0.1:8000/api/chat/thread/ (Thread List and create new thread)
4. http://127.0.0.1:8000/api/chat/thread/int:pk/ (Detail of thread)
5. http://127.0.0.1:8000/api/chat/thread/int:pk/messages/ (Message list of thread and create new message)
6. http://127.0.0.1:8000/api/chat/message/ (Message list of all thread and create new message) * where is the user
7. http://127.0.0.1:8000/api/chat/message/int:pk/ (Detail of message)
8. http://127.0.0.1:8000/api/chat/message/int:pk/mark_as_read/ (Update Message.is_read = True) * use post method
9. http://127.0.0.1:8000/api/chat/unread_message_count/ (Count of unread message)
