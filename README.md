# drf_project!

Here is Django REST framework hw:

Root - $ http http://127.0.0.1:8000/api/

Generate token - $ http POST http://127.0.0.1:8000/user/api-token-auth/ username="***" password="***"
Create post with token - $ http POST http://127.0.0.1:8000/api/post/ title='***' text='***' 'Authorization: Token ***'
Create comment with token - $ http POST http://127.0.0.1:8000/api/comments/ text='***' post='http://127.0.0.1:8000/api/post/1/' 'Authorization: Token ***'- 
Update - $ http PUT http://127.0.0.1:8000/api/post/4/ title='****', text='****' 'Authorization: Token ****'
Delete - $ http DELETE http://127.0.0.1:8000/api/post/1/ 'Authorization: Token '***'
