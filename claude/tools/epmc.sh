epmc() {
  local q="$1" rt="${2:-lite}" ps="${3:-25}" code
  for i in 1 2 3 4 5 6; do
    code=$(curl -s -o /tmp/claude-0/epmc.json -w "%{http_code}" -G \
      "https://www.ebi.ac.uk/europepmc/webservices/rest/search" \
      --data-urlencode "query=$q" --data-urlencode "resultType=$rt" \
      --data-urlencode 'format=json' --data-urlencode "pageSize=$ps")
    if [ "$code" = "200" ]; then
      if python3 -c "import json,sys; d=json.load(open('/tmp/claude-0/epmc.json')); sys.exit(0 if 'hitCount' in d else 1)" 2>/dev/null; then
        return 0
      fi
      echo "epmc: HTTP 200 but body has no hitCount (attempt $i) — retrying" >&2
    else
      echo "epmc: HTTP $code (attempt $i) — retrying" >&2
    fi
    sleep 15
  done
  echo "epmc: FAILED after 6 attempts — query: $q" >&2; return 1
}
