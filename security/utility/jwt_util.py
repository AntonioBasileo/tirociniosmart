import base64
import hashlib
import hmac
import json
import time


class JWTError(Exception):
    pass


class JWTExpired(JWTError):
    pass


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode((data + padding).encode("ascii"))


def _sign_hs256(message: bytes, secret: str) -> str:
    sig = hmac.new(secret.encode("utf-8"), message, hashlib.sha256).digest()
    return _b64url_encode(sig)


def encode_jwt(payload: dict, secret: str) -> str:
    header = {"typ": "JWT", "alg": "HS256"}
    header_b64 = _b64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    payload_b64 = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))

    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    signature_b64 = _sign_hs256(signing_input, secret)

    return f"{header_b64}.{payload_b64}.{signature_b64}"


def decode_jwt(token: str, secret: str, issuer: str = None) -> dict:
    parts = token.split(".")
    if len(parts) != 3:
        raise JWTError("Invalid token format")

    header_b64, payload_b64, signature_b64 = parts
    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")

    expected_sig = _sign_hs256(signing_input, secret)
    if not hmac.compare_digest(expected_sig, signature_b64):
        raise JWTError("Invalid signature")

    payload = json.loads(_b64url_decode(payload_b64).decode("utf-8"))

    now = int(time.time())
    exp = payload.get("exp")
    if exp is not None and now >= int(exp):
        raise JWTExpired("Token expired")

    if issuer is not None:
        iss = payload.get("issuer")
        if iss != issuer:
            raise JWTError("Invalid issuer")

    return payload