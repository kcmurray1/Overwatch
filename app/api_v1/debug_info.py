import random

CPU_OPTIONS = ["Intel(R) Core(TM) i5-8500 CPU @ 3.00GHz", "Intel(R) Core(TM) i5-8400 CPU @ 2.80GHz", "Intel(R) Core(TM) i7-7700 CPU @ 3.60GHz"]
MAN_OPTIONS = ["Dell Inc.", "IBuyPower", "HP"]
OS_TYPE_OPTIONS = ["windows", "linux"]
OS_OPTIONS = ["Microsoft Windows 11 Pro", "Ubuntu 22.04 LTS", "Microsoft Windows 10 Home"]
USER_OPTIONS = ["kman", "bobby", "alice"]
MODEL_OPTIONS = ["Dell Inc. Inspiron 3670", "Precision Tower 3430", "Fracture"]
def generate_mock_machine(count):
    """Generate machines from options of configurations. Used to debug frontend"""
    machines = list()

    for i in range(count):
        addr = f"10.0.0.{random.randint(1,255)}"
        cpu = random.choice(CPU_OPTIONS)
        id = i
        manufacturer = random.choice(MAN_OPTIONS)
        model = random.choice(MODEL_OPTIONS)
        os = random.choice(OS_OPTIONS)
        os_type = random.choice(OS_TYPE_OPTIONS)
        port = random.randint(1000,9999)
        user = random.choice(USER_OPTIONS)
        is_online = random.choice([True, False])

        machines.append({ "address": addr,
        "cpu": cpu,
        "id": id,
        "manufacturer": manufacturer,
        "model": model,
        "os": os,
        "os_type": os_type,
        "port": port,
        "user": user,
        "is_online": is_online
        })
    
    return machines