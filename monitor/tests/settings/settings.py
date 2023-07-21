from core.config import settings

BASE_URI = 'monitor:5000'

auth_create_url: str = f'http://{BASE_URI}/api/v1/auth/user_create'
auth_login_url: str = f'http://{BASE_URI}/api/v1/auth/login'
monitor_post_url: str = f'http://{BASE_URI}/api/v1/monitor/one_link'
monitor_get_urls: str = f'http://{BASE_URI}/api/v1/monitor/links'
monitor_post_urls: str = f'http://{BASE_URI}/api/v1/monitor/links'
monitor_post_image: str = f'http://{BASE_URI}/api/v1/monitor/file_upload'
monitor_get_logs: str = f'http://{BASE_URI}/api/v1/monitor/logs'
web_get_links: str = f'http://{BASE_URI}/web/links'
web_get_register: str = f'http://{BASE_URI}/web/auth/register'
web_get_logs: str = f'http://{BASE_URI}/web/logs'
redis_url: str = settings.redis.url
pg_async_url: str = settings.db.url_async
