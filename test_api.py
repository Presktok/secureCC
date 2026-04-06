import urllib.request
import json
import traceback

data = {'code': 'int main() { char *buf = malloc(10); free(buf); printf(buf); int *x; x = buf; free(x); }'}
req = urllib.request.Request('http://localhost:8000/compile', method='POST', headers={'Content-Type': 'application/json'}, data=json.dumps(data).encode())

try:
    resp = urllib.request.urlopen(req)
    out = resp.read().decode("utf-8", errors="replace")
    with open("api_out.txt", "w", encoding="utf-8") as f:
        f.write(out)
except Exception as e:
    with open("api_err.txt", "w", encoding="utf-8") as f:
        f.write(str(e) + "\n")
        if hasattr(e, 'read'):
            f.write(e.read().decode("utf-8", errors="replace"))
