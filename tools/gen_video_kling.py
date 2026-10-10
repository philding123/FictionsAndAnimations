#!/usr/bin/env python3
"""可灵（Kling）图生视频工具：关键帧 → 视频任务（创建 + 轮询 + 下载）。

用法:
    python tools/gen_video_kling.py --image <hd关键帧.png> --prompt "运镜与画面描述" \
        [--duration 5|10] [--mode std|pro] [--model kling-v1-6] [--out out.mp4] [--timeout 900]

凭证（~/.config/Fiction/env，三选一）：
  1. KLING=<api key>            → Bearer 直连（国内开发者平台「API 密钥」，api-key-kling-... 格式）
  2. KLING_AK=<access key> + KLING_SK=<secret key> → 官方开放平台 JWT(HS256) 签名
端点（2026-10-10 实测）：国内开发者平台账号用 https://api-beijing.klingai.com
（api.klingai.com 与 api-singapore.klingai.com 对国内 key 均 401）。
当前可用模型：kling-v2-5-turbo、kling-v2-6（v1.x/v2-master 已下线）；
429 "Account balance not enough" = API 额度/资源包未充值（与 App 会员相互独立）。
任务为异步：POST /v1/videos/image2video 创建，轮询 GET 同路径/{id}。
"""
import argparse
import base64
import hashlib
import hmac
import json
import sys
import time
import urllib.request
from pathlib import Path

KEY_PATH = Path.home() / ".config" / "Fiction" / "env"
BASES = ["https://api-beijing.klingai.com", "https://api-singapore.klingai.com"]


def _b64url(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


def sign_jwt(ak: str, sk: str) -> str:
    headers = {"alg": "HS256", "typ": "JWT"}
    now = int(time.time())
    payload = {"iss": ak, "exp": now + 1800, "nbf": now - 5}
    signing_input = f"{_b64url(json.dumps(headers).encode())}.{_b64url(json.dumps(payload).encode())}"
    sig = hmac.new(sk.encode(), signing_input.encode(), hashlib.sha256).digest()
    return f"{signing_input}.{_b64url(sig)}"


def load_auth() -> tuple[str, str | None]:
    """返回 (token, 说明)。支持 KLING= 单 key 或 KLING_AK/KLING_SK= JWT 模式。"""
    cfg = {}
    for line in KEY_PATH.read_text(encoding="utf-8").splitlines():
        k, _, v = line.strip().partition("=")
        if k.strip():
            cfg[k.strip()] = v.strip()
    if cfg.get("KLING_AK") and cfg.get("KLING_SK"):
        return sign_jwt(cfg["KLING_AK"], cfg["KLING_SK"]), "JWT(KLING_AK/KLING_SK)"
    if cfg.get("KLING"):
        return cfg["KLING"], "Bearer(KLING)"
    raise SystemExit(f"错误：{KEY_PATH} 中没有 KLING= 或 KLING_AK/KLING_SK= 配置")


def request(base: str, method: str, path: str, key: str, payload: dict | None = None):
    url = base + path
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {key}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:500]
        return e.code, {"error": body}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True)
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--negative", default="")
    ap.add_argument("--duration", default="5", choices=["5", "10"])
    ap.add_argument("--mode", default="std", choices=["std", "pro"])
    ap.add_argument("--model", default="kling-v2-5-turbo")
    ap.add_argument("--out", required=True)
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--poll", type=int, default=10)
    args = ap.parse_args()

    key = load_key()
    img_b64 = base64.b64encode(Path(args.image).read_bytes()).decode()
    payload = {
        "model_name": args.model,
        "image": img_b64,
        "prompt": args.prompt,
        "negative_prompt": args.negative,
        "cfg_scale": 0.5,
        "mode": args.mode,
        "duration": args.duration,
    }

    status = resp = None
    work_base = None
    for base in BASES:
        status, resp = request(base, "POST", "/v1/videos/image2video", key, payload)
        print(f"[{base}] POST -> {status}")
        if status in (200, 201):
            work_base = base
            break
        msg = json.dumps(resp, ensure_ascii=False)[:300]
        print("  ", msg)
        if status == 429 or "balance" in msg.lower():
            raise SystemExit(
                "错误：API 账户余额/资源包不足（与 App 会员相互独立）。\n"
                "请到可灵开发者平台「API购买入口 / 资源包管理」充值后重试。")
        if status == 404:
            continue  # 换端点/模型重试
    else:
        raise SystemExit("错误：所有端点均创建任务失败")

    task_id = (resp.get("data") or {}).get("task_id")
    if not task_id:
        raise SystemExit(f"错误：响应中没有 task_id：{json.dumps(resp, ensure_ascii=False)[:300]}")
    print(f"task_id: {task_id}")

    t0 = time.time()
    while True:
        time.sleep(args.poll)
        status, resp = request(work_base, "GET", f"/v1/videos/image2video/{task_id}", key)
        data = resp.get("data") or {}
        st = data.get("task_status")
        print(f"  [{int(time.time()-t0)}s] {st}")
        if st == "succeed":
            videos = (data.get("task_result") or {}).get("videos") or []
            if not videos:
                raise SystemExit(f"错误：任务成功但没有视频：{json.dumps(data, ensure_ascii=False)[:300]}")
            url = videos[0]["url"]
            print("下载:", url[:100], "...")
            urllib.request.urlretrieve(url, args.out)
            print(f"OK: {args.out}  {Path(args.out).stat().st_size/1024:.0f} KB")
            return
        if st == "failed":
            raise SystemExit(f"错误：任务失败：{json.dumps(data, ensure_ascii=False)[:400]}")
        if time.time() - t0 > args.timeout:
            raise SystemExit(f"错误：超时（{args.timeout}s），最后状态 {st}")


if __name__ == "__main__":
    main()
