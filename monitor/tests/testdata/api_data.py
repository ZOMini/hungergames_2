user_create_data = {
    "email": "test@ya.ru",
    "name": "testuser",
    "password": "testpass",
    "password2": "testpass"}
user_login_data = {
    "email": "test@ya.ru",
    "password": "testpass"}
monitor_url_post_data = {
    "url": "http://abc.hostname.com/somethings/anything/qqq12345678/?sodfdme_key=som2e_value&2wqeqwe=fsdgd2sf",}
monitor_url_post_response = {
    "domain": "abc.hostname",
    "params": {
        "2wqeqwe": [
        "fsdgd2sf"
        ],
        "sodfdme_key": [
        "som2e_value"
        ]
    },
    "path": "/somethings/anything/qqq12345678/",
    "protocol": "http",
    "suffix": "com"
    }
monitor_url_get_data = {'page': 0, 'size': 4, 'domain_zone': 'com'}
