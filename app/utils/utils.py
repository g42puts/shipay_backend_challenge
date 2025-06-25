from datetime import datetime


claims = {
    "user:create": "user:create",
    "user:list": "user:list",
    "user:view": "user:view",
    "user:update": "user:update",
    "user:delete": "user:delete",
    "user:claim:add": "user:claim:add",
    "user:claim:remove": "user:claim:remove",
    "role:list": "role:list",
    "role:view": "role:view",
    "role:update": "role:update",
    "role:delete": "role:delete",
    "claim:create": "claim:create",
    "claim:list": "claim:list",
    "claim:view": "claim:view",
    "claim:update": "claim:update",
    "claim:delete": "claim:delete",
}


def get_current_datetime_formatted():
    return datetime.now().strftime(format="%m/%d/%Y, %H:%M:%S")
