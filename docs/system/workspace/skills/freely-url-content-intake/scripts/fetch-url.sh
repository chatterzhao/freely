#!/usr/bin/env bash
set -euo pipefail

url="${1:-}"
curl_bin="${CURL_BIN:-curl}"

if [[ -z "$url" ]]; then
  echo "fetch_status=failed"
  echo "content_kind=unknown"
  echo "failure_reason=missing_url"
  echo "recommended_next_step=provide_a_http_or_https_url"
  exit 1
fi

fetch_wechat_article() {
  "$curl_bin" -sL \
    -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
    -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
    -H "Accept-Language: zh-CN,zh;q=0.9,en;q=0.8" \
    "$1"
}

fetch_generic_url() {
  "$curl_bin" -sL "$1"
}

case "$url" in
  https://mp.weixin.qq.com/s/*|http://mp.weixin.qq.com/s/*|https://mp.weixin.qq.com/*|http://mp.weixin.qq.com/*)
    echo "fetch_status=ok"
    echo "content_kind=wechat_article"
    echo "failure_reason="
    echo "recommended_next_step=extract_readable_content_or_detect_block_page"
    fetch_wechat_article "$url"
    ;;
  http://*|https://*)
    echo "fetch_status=ok"
    echo "content_kind=webpage"
    echo "failure_reason="
    echo "recommended_next_step=extract_readable_content"
    fetch_generic_url "$url"
    ;;
  *)
    echo "fetch_status=unsupported"
    echo "content_kind=unknown"
    echo "failure_reason=unsupported_scheme_or_platform"
    echo "recommended_next_step=use_a_http_or_https_url"
    exit 2
    ;;
esac
