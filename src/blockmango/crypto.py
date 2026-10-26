from __future__ import annotations

import base64
import hashlib
import json
import time
import uuid
from typing import Any, Callable

try:
    from Crypto.Cipher import PKCS1_v1_5
    from Crypto.PublicKey import RSA
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False
    PKCS1_v1_5 = None
    RSA = None

from .constants import (
    APP_MD5,
    DEVICE_HEADER_PATHS,
    RAW_SIGN_PATHS,
    RAW_SIGN_PATH_PREFIXES,
    RSA_KEY,
)
from .exceptions import CryptoError

TokenEncoder = Callable[[str, str, str, str, str, str, str], str]
"""Optional callback that returns a per-request Access-Token header value."""


def _md5(data: str | bytes) -> str:
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.md5(data).hexdigest()


def _enc_password(plain: str) -> str:
    if not HAS_CRYPTO:
        raise CryptoError("pycryptodome is required for RSA encryption")
    key = RSA.import_key(RSA_KEY)
    cipher = PKCS1_v1_5.new(key)
    return base64.b64encode(cipher.encrypt(plain.encode())).decode()


def _compact(obj: dict[str, Any] | list[Any] | None) -> str:
    if obj is None:
        return ""
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=False)


def _flatten_params(params: dict[str, Any]) -> list[tuple[str, str]]:
    flat: list[tuple[str, str]] = []
    for k in sorted(params):
        v = params[k]
        if isinstance(v, (list, tuple)):
            for item in v:
                flat.append((k, str(item)))
        else:
            flat.append((k, str(v)))
    return flat


def _params_to_string(flat: list[tuple[str, str]]) -> str:
    return "&".join(f"{k}={v}" for k, v in flat)


def _is_raw_sign_path(path: str) -> bool:
    return path in RAW_SIGN_PATHS or path.startswith(RAW_SIGN_PATH_PREFIXES)


def _sign(
    path: str, params: list[tuple[str, str]], body: str,
    ak: str, sk: str, device_id: str | None, t_off: int,
) -> tuple[str, str, str]:
    nonce = str(uuid.uuid4())
    ts = str(int(time.time()) + t_off)
    ps = _params_to_string(params)
    base = ak + path + nonce + ts + ps + body + sk
    if _is_raw_sign_path(path):
        sign = _md5(base)
    else:
        if not device_id:
            raise CryptoError("device_id required for this endpoint")
        sign = _md5(_md5(base) + device_id)
    return nonce, ts, sign


def _build_signed_headers(
    path: str, flat_params: list[tuple[str, str]], body_str: str,
    ak: str, sk: str, device_id: str, device_sign: str,
    t_off: int, uid: int | None = None, token: str | None = None,
    language: str | None = None, app_headers: dict[str, str] | None = None,
    region: str | None = None, uid_register_ts: str | int | None = None,
    device_register_ts: str | int | None = None,
    device_headers: dict[str, str] | None = None,
    token_encoder: TokenEncoder | None = None,
) -> dict[str, str]:
    nonce, ts, sign = _sign(path, flat_params, body_str, ak, sk, device_id, t_off)
    headers: dict[str, str] = dict(app_headers) if app_headers else {}
    if device_headers:
        headers.update(device_headers)
    headers.update({
        "x-apikey": ak,
        "x-nonce": nonce,
        "x-time": ts,
        "x-sign": sign,
        "x-urlpath": path,
        "userdeviceid": device_id,
        "md5": APP_MD5,
    })
    if region:
        headers["region"] = region
    if uid_register_ts is not None:
        headers["uid_register_ts"] = str(uid_register_ts)
    if device_register_ts is not None:
        headers["device_register_ts"] = str(device_register_ts)
    if path in DEVICE_HEADER_PATHS:
        headers["bmg-device-id"] = device_id
        headers["bmg-sign"] = device_sign
    if body_str:
        headers.setdefault("content-length", str(len(body_str.encode("utf-8"))))
    if uid is not None and token:
        headers["userid"] = str(uid)
        token_value = token
        if token_encoder is not None:
            try:
                token_value = token_encoder(
                    token, path, nonce, ts,
                    _params_to_string(flat_params), body_str, region or "",
                )
            except Exception:
                token_value = token
        headers["access-token"] = token_value
    if language:
        headers["language"] = language
    return headers
