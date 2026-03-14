import base64
import hashlib
import hmac
import json
import os
import secrets
import time

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import (
    create_user_with_password,
    get_auth_user_by_email,
    get_role_by_name,
)
from app.schemas import (
    AuthUserResponse,
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
)

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-key")
JWT_ALGORITHM = "HS256"
PARTICIPANT_ROLE_NAME = "participant"
PASSWORD_HASH_NAME = "pbkdf2_sha256"
PASSWORD_HASH_ITERATIONS = 100000


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        PASSWORD_HASH_ITERATIONS,
    )
    return (
        f"{PASSWORD_HASH_NAME}${PASSWORD_HASH_ITERATIONS}"
        f"${_b64url_encode(salt)}${_b64url_encode(password_hash)}"
    )


def verify_password(password: str, password_hash: str) -> bool:
    try:
        algorithm, iterations_raw, salt_raw, expected_hash_raw = password_hash.split("$")
    except ValueError:
        return False

    if algorithm != PASSWORD_HASH_NAME:
        return False

    calculated_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        _b64url_decode(salt_raw),
        int(iterations_raw),
    )
    expected_hash = _b64url_decode(expected_hash_raw)
    return hmac.compare_digest(calculated_hash, expected_hash)


def create_access_token(user_id: int) -> str:
    header = {"alg": JWT_ALGORITHM, "typ": "JWT"}
    payload = {
        "sub": str(user_id),
        "exp": int(time.time()) + ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }

    encoded_header = _b64url_encode(
        json.dumps(header, separators=(",", ":"), sort_keys=True).encode()
    )
    encoded_payload = _b64url_encode(
        json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    )
    signing_input = f"{encoded_header}.{encoded_payload}".encode()
    signature = hmac.new(
        JWT_SECRET_KEY.encode(),
        signing_input,
        hashlib.sha256,
    ).digest()
    return f"{encoded_header}.{encoded_payload}.{_b64url_encode(signature)}"


def decode_access_token(token: str) -> int:
    try:
        encoded_header, encoded_payload, encoded_signature = token.split(".")
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        ) from exc

    signing_input = f"{encoded_header}.{encoded_payload}".encode()
    expected_signature = hmac.new(
        JWT_SECRET_KEY.encode(),
        signing_input,
        hashlib.sha256,
    ).digest()

    if not hmac.compare_digest(_b64url_encode(expected_signature), encoded_signature):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    try:
        payload = json.loads(_b64url_decode(encoded_payload))
    except (ValueError, json.JSONDecodeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        ) from exc

    expires_at = payload.get("exp")
    subject = payload.get("sub")

    if not isinstance(expires_at, int) or expires_at < int(time.time()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )

    if subject is None or not str(subject).isdigit():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    return int(subject)


def build_full_name(first_name: str, last_name: str) -> str:
    return f"{first_name.strip()} {last_name.strip()}".strip()


async def register_user(
    session: AsyncSession,
    payload: RegisterRequest,
) -> RegisterResponse:
    existing_user = await get_auth_user_by_email(session, payload.email)
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    participant_role = await get_role_by_name(session, PARTICIPANT_ROLE_NAME)
    if participant_role is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Participant role is not configured",
        )

    try:
        user = await create_user_with_password(
            session,
            email=payload.email,
            full_name=build_full_name(payload.firstName, payload.lastName),
            university=payload.university,
            role_id=participant_role.id,
            password_hash=hash_password(payload.password),
        )
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        ) from exc

    token = create_access_token(user.id)
    return RegisterResponse(
        id=str(user.id),
        email=user.email,
        role=PARTICIPANT_ROLE_NAME,
        token=token,
    )


async def login_user(
    session: AsyncSession,
    payload: LoginRequest,
) -> LoginResponse:
    user = await get_auth_user_by_email(session, payload.email)
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(user.id)
    return LoginResponse(
        token=token,
        user=AuthUserResponse(
            id=str(user.id),
            email=user.email,
            role=user.role_name,
        ),
    )
