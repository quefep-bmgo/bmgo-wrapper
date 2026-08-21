from __future__ import annotations

import base64
import hashlib
import json
import uuid
from typing import Any

try:
    from Crypto.Cipher import PKCS1_v1_5
    from Crypto.PublicKey import RSA
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False
    PKCS1_v1_5 = None
    RSA = None

from .constants import RSA_KEY
from .exceptions import CryptoError


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


def _sign(
    path: str, params: list[tuple[str, str]], body: str,
    ak: str, sk: str, device_id: str | None, t_off: int,
) -> tuple[str, str, str]:
    nonce = str(uuid.uuid4())
    ts = str(int(__import__("time").time()) + t_off)
    ps = _params_to_string(params)
    base = ak + path + nonce + ts + ps + body + sk
    if path.startswith("/user/api/v4/account/"):
        sign = _md5(base)
    else:
        if not device_id:
            raise CryptoError("device_id required for non-account endpoint signing")
        sign = _md5(_md5(base) + device_id)
    return nonce, ts, sign


def _build_signed_headers(
    path: str, flat_params: list[tuple[str, str]], body_str: str,
    ak: str, sk: str, device_id: str, device_sign: str,
    t_off: int, uid: int | None = None, token: str | None = None,
    language: str | None = None, app_headers: dict[str, str] | None = None,
) -> dict[str, str]:
    nonce, ts, sign = _sign(path, flat_params, body_str, ak, sk, device_id, t_off)
    headers: dict[str, str] = dict(app_headers) if app_headers else {}
    headers.update({
        "Host": "gw.sandboxol.com", "bmg-device-id": device_id,
        "bmg-sign": device_sign, "x-apikey": ak, "x-nonce": nonce,
        "x-time": ts, "x-sign": sign, "x-urlpath": path,
    })
    if body_str:
        headers["md5"] = _md5(body_str)
    if uid is not None and token:
        headers["userid"] = str(uid)
        headers["access-token"] = token
    if language:
        headers["language"] = language
    return headers