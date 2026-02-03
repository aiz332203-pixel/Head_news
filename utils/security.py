import hashlib

from passlib.context import CryptContext

#创建密码上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def get_hash_password(password: str):
#     """生成密码哈希"""
#     return pwd_context.hash(password)


def get_hash_password(password: str) -> str:
    """生成哈希密码，处理长密码问题"""
    # 如果密码过长，先使用SHA256进行预哈希
    if isinstance(password, str):
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            # 使用SHA256预哈希，确保长度不超过72字节
            sha256_hash = hashlib.sha256(password_bytes).hexdigest()
            # 使用固定长度的字符串作为bcrypt的输入
            password = sha256_hash

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    original_password = plain_password

    if isinstance(plain_password, str):
        password_bytes = plain_password.encode('utf-8')
        if len(password_bytes) > 72:
            # 如果原始密码超过72字节，使用相同的预哈希方法
            sha256_hash = hashlib.sha256(password_bytes).hexdigest()
            plain_password = sha256_hash

    return pwd_context.verify(plain_password, hashed_password)