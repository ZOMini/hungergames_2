from sqlalchemy.sql import select

from core.app import jwt
from db.connection_db import db_session
from db.connection_redis import jwt_redis_blocklist
from db.models_db import User


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return db_session.scalar(select(User).filter(User.id == identity).limit(1))

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(_jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None
