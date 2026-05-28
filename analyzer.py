import sys
import json
from collections import defaultdict

def parse_time(t):
    if t.endswith("ms"):
        return int(t.replace("ms", ""))
    if t.endswith("s"):
        return int(float(t.replace("s", "")) * 1000)
    try:
        return int(t)
    except:
        return None

def parse_line(line):
    line = line.strip()

    if not line:
        return None, True

    # JSON format
    try:
        data = json.loads(line)
        return {
            "path": data.get("path"),
            "status": data.get("status"),
            "time": None
        }, False
    except:
        pass

    parts = line.split()

    path = None
    status = None
    time = None

    # find path (most reliable anchor)
    for p in parts:
        if p.startswith("/api"):
            path = p
            break

    # find status (3-digit number or '-')
    for p in parts:
        cleaned = p.strip(",[]()\"")

        if cleaned == "-":
            continue

        if cleaned.isdigit() and len(cleaned) == 3:
            status = int(cleaned)
            break

    # time = last parseable token
    for p in reversed(parts):
        t = parse_time(p.strip(",[]()\""))
        if t is not None:
            time = t
            break

    if not path:
        return None, True

    return {
        "path": path,
        "status": status,
        "time": time
    }, False

def analyze(file_path):
    total = 0
    malformed = 0

    endpoint_count = defaultdict(int)
    slowest = defaultdict(list)
    errors = defaultdict(int)

    with open(file_path, "r") as f:
        for line in f:
            total += 1
            parsed, is_bad = parse_line(line)

            if is_bad or not parsed:
                malformed += 1
                continue

            path = parsed["path"]
            status = parsed["status"]
            time = parsed["time"]

            if path:
                endpoint_count[path] += 1

            if path and time:
                slowest[path].append(time)

            if status and status >= 400:
                errors[status] += 1

    print(f"Total Lines: {total}")
    print(f"Malformed Lines: {malformed}\n")

    print("Top Endpoints:")
    for k, v in sorted(endpoint_count.items(), key=lambda x: -x[1])[:5]:
        print(f"{k}: {v}")

    print("\nSlowest Endpoints (avg ms):")
    for k, v in slowest.items():
        if v:
            print(f"{k}: {sum(v)//len(v)}")

    print("\nErrors:")
    for k, v in errors.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyzer.py data/sample.log")
        sys.exit(1)

    analyze(sys.argv[1])