# epmc_all QUERY OUTFILE [RESULTTYPE] [PAGESIZE] — cursorMark paging, collects ALL hits, verifies the count.
epmc_all() {
  local q="$1" out="$2" rt="${3:-core}" ps="${4:-100}" cur='*' n=0 hc=-1 got nxt code tries
  : > "${out}.parts"
  while : ; do
    tries=0
    while [ "$tries" -lt 6 ]; do
      code=$(curl -s -o /tmp/claude-0/_pg.json -w "%{http_code}" -G \
        "https://www.ebi.ac.uk/europepmc/webservices/rest/search" \
        --data-urlencode "query=$q" --data-urlencode "resultType=$rt" \
        --data-urlencode 'format=json' --data-urlencode "pageSize=$ps" \
        --data-urlencode "cursorMark=$cur")
      if [ "$code" = "200" ] && python3 -c "import json,sys;d=json.load(open('/tmp/claude-0/_pg.json'));sys.exit(0 if 'resultList' in d else 1)" 2>/dev/null; then break; fi
      echo "epmc_all: HTTP $code / bad body (try $((tries+1))) — retrying" >&2; sleep 15; tries=$((tries+1))
    done
    if [ "$tries" -ge 6 ]; then echo "epmc_all: FAILED after retries" >&2; return 1; fi
    python3 -c "
import json
d=json.load(open('/tmp/claude-0/_pg.json'))
open('/tmp/claude-0/_meta','w').write('%d\n%s\n%d\n'%(len(d['resultList'].get('result',[])), d.get('nextCursorMark',''), d.get('hitCount',0)))
"
    got=$(sed -n 1p /tmp/claude-0/_meta); nxt=$(sed -n 2p /tmp/claude-0/_meta); hc=$(sed -n 3p /tmp/claude-0/_meta)
    cat /tmp/claude-0/_pg.json >> "${out}.parts"; echo >> "${out}.parts"
    n=$((n+got))
    echo "  page: +$got  total=$n / $hc" >&2
    [ "$got" -eq 0 ] && break
    [ -z "$nxt" ] && break
    [ "$nxt" = "$cur" ] && break
    [ "$n" -ge "$hc" ] && break
    cur="$nxt"
  done
  python3 - "${out}.parts" "$out" <<'PY'
import json,sys
recs=[]
for line in open(sys.argv[1],encoding='utf-8'):
    line=line.strip()
    if not line: continue
    recs.extend(json.loads(line)['resultList'].get('result',[]))
seen={}
for r in recs: seen[r.get('id') or r.get('doi') or json.dumps(r)[:80]]=r
json.dump(list(seen.values()),open(sys.argv[2],'w',encoding='utf-8'))
print("collected",len(recs),"unique",len(seen))
PY
  echo "epmc_all: hitCount=$hc collected=$n SHORTFALL=$((hc-n))"
}
