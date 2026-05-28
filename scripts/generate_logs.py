import random
from datetime import datetime
import json

number_of_logs = 1000

methods = ["GET", "POST", "PUT"]
paths = ["/api/users", "/api/login", "/api/products"]
statuses = [200, 201, 400, 401, 404, 500]

def random_ip():
    return ".".join(str(random.randint(1, 255)) for _ in range(4))

def random_timestamp():
    formats = [
        lambda: datetime.now().isoformat() + "Z",
        lambda: datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        lambda: datetime.now().strftime("%d-%b-%Y %H:%M:%S"),
        lambda: str(int(datetime.now().timestamp()))
    ]
    return random.choice(formats)()

def random_time():
    formats = [
        lambda: f"{random.randint(10,500)}ms",
        lambda: f"{random.random():.3f}s",
        lambda: str(random.randint(10,500))
    ]
    return random.choice(formats)()

def extra_fields():
    return f'"Mozilla/5.0" "https://example.com/ref"'

def generate_line():
    t = random_timestamp()
    ip = random_ip()
    method = random.choice(methods)
    path = random.choice(paths)
    status = random.choice(statuses)
    time = random_time()

    if random.random() < 0.3:
        return f"{t} {ip} {method} {path} {status} {time} {extra_fields()}"
    else:
        return f"{t} {ip} {method} {path} {status} {time}"

def generate_bad_line():
    options = [
        "BROKEN LINE",
        "",
        f"{random.randint(1000000000,2000000000)} {random_ip()} GET /api/test - 0.1s",
        json.dumps({"timestamp": "2024-03-15T14:23:01Z", "status": 200}),
    ]
    return random.choice(options)

with open("data/sample.log", "w") as f:
    for _ in range(number_of_logs):
        if random.random() < 0.1:
            f.write(generate_bad_line() + "\n")
        else:
            f.write(generate_line() + "\n")