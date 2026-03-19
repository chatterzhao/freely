#!/usr/bin/env bash
set -euo pipefail

input="${1:-/dev/stdin}"
kind="${2:-webpage}"

extract_wechat_article() {
  perl -0ne '
    if (/<div[^>]+id="js_content"[^>]*>(.*)<\/div>\s*<script/is) {
      print $1;
      exit 0;
    }
    exit 1;
  ' "$1" | perl -0pe '
    s/<script\b[^>]*>.*?<\/script>//gis;
    s/<style\b[^>]*>.*?<\/style>//gis;
    s/<br\s*\/?>/\n/gis;
    s/<\/p>/\n\n/gis;
    s/<\/section>/\n/gis;
    s/<[^>]+>/ /g;
    s/&nbsp;/ /g;
    s/&amp;/\&/g;
    s/&quot;/"/g;
    s/&#39;/'\''/g;
    s/\s+\n/\n/g;
    s/\n{3,}/\n\n/g;
    s/[ \t]{2,}/ /g;
    s/^\s+|\s+$//g;
  '
}

extract_generic_html() {
  perl -0pe '
    s/<script\b[^>]*>.*?<\/script>//gis;
    s/<style\b[^>]*>.*?<\/style>//gis;
    s/<br\s*\/?>/\n/gis;
    s/<\/p>/\n\n/gis;
    s/<[^>]+>/ /g;
    s/&nbsp;/ /g;
    s/&amp;/\&/g;
    s/&quot;/"/g;
    s/&#39;/'\''/g;
    s/\s+\n/\n/g;
    s/\n{3,}/\n\n/g;
    s/[ \t]{2,}/ /g;
    s/^\s+|\s+$//g;
  ' "$1"
}

case "$kind" in
  wechat_article)
    extract_wechat_article "$input"
    ;;
  webpage)
    extract_generic_html "$input"
    ;;
  *)
    echo "unsupported content kind: $kind" >&2
    exit 2
    ;;
esac
