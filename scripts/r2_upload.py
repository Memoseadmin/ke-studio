#!/usr/bin/env python3
"""카드 이미지를 Cloudflare R2(S3 호환)에 올리고 공개 URL 목록을 urls.json에 쓴다. 기본 dry-run.

  python3 scripts/r2_upload.py cardnews/posts/2026-10-09            # dry-run
  python3 scripts/r2_upload.py cardnews/posts/2026-10-09 --execute  # 실제 업로드

키: cardnews/<YYYY-MM-DD>/card-NN.png  (날짜 = post_dir 이름)
환경변수: R2_ACCOUNT_ID, R2_ACCESS_KEY_ID(비밀), R2_SECRET_ACCESS_KEY(비밀), R2_BUCKET, IMAGE_HOST_BASE_URL
값은 출력하지 않는다. boto3 필요(pip install boto3, 실행 시에만 import).
"""
import argparse, glob, json, os, sys
from pathlib import Path

NEED = ["R2_ACCOUNT_ID", "R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY", "R2_BUCKET", "IMAGE_HOST_BASE_URL"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("post_dir")
    ap.add_argument("--dry-run", action="store_true", help="기본값")
    ap.add_argument("--execute", action="store_true")
    a = ap.parse_args()
    d = Path(a.post_dir)
    date = d.resolve().name
    files = sorted(glob.glob(str(d / "card-[0-9][0-9].png")))
    if not files:
        sys.exit("card-NN.png 없음")
    base = os.environ.get("IMAGE_HOST_BASE_URL", "<IMAGE_HOST_BASE_URL>").rstrip("/")
    plan = [(f, f"cardnews/{date}/{os.path.basename(f)}") for f in files]
    urls = [f"{base}/{k}" for _, k in plan]
    print(f"[{'EXECUTE' if a.execute else 'DRY-RUN'}] bucket={os.environ.get('R2_BUCKET', '<R2_BUCKET>')}")
    print("env:", {v: ("SET" if os.environ.get(v) else "UNSET") for v in NEED})
    for (f, k), u in zip(plan, urls):
        print(f"  PUT {k}  <- {os.path.basename(f)}\n      public: {u}")
    if not a.execute:
        print(f"urls.json 에 쓸 내용: {len(urls)}개 URL (dry-run이라 쓰지 않음)")
        return
    missing = [v for v in NEED if not os.environ.get(v)]
    if missing:
        sys.exit("UNSET: " + ", ".join(missing))
    import boto3
    s3 = boto3.client("s3", endpoint_url=f"https://{os.environ['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com",
                      aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
                      aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"], region_name="auto")
    for f, k in plan:
        s3.upload_file(f, os.environ["R2_BUCKET"], k, ExtraArgs={"ContentType": "image/png"})
    (d / "urls.json").write_text(json.dumps(urls, ensure_ascii=False, indent=2) + "\n")
    print(f"uploaded {len(urls)} files; wrote {d / 'urls.json'}")


if __name__ == "__main__":
    main()
