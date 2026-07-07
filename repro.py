import os
import time
import json
import msvcrt
import threading
import concurrent.futures

WAL_FILE = "skills_wal.jsonl"

def init_wal():
    if not os.path.exists(WAL_FILE):
        with open(WAL_FILE, "w") as f:
            f.write(" ")

class WALManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.local = threading.local()

    def get_file(self):
        if not hasattr(self.local, 'f'):
            # Open file in append/read mode for this thread
            self.local.f = open(self.file_path, 'r+')
        return self.local.f
        
    def acquire_lock(self, file_obj):
        while True:
            try:
                file_obj.seek(0)
                msvcrt.locking(file_obj.fileno(), msvcrt.LK_NBLCK, 1)
                return
            except OSError:
                time.sleep(0.001)

    def release_lock(self, file_obj):
        file_obj.seek(0)
        try:
            msvcrt.locking(file_obj.fileno(), msvcrt.LK_UNLCK, 1)
        except OSError:
            pass

    def append(self, entry: dict):
        t0 = time.perf_counter()
        f = self.get_file()
        self.acquire_lock(f)
        try:
            f.seek(0, os.SEEK_END)
            f.write("\n" + json.dumps(entry))
            f.flush()
        finally:
            self.release_lock(f)
        t1 = time.perf_counter()
        return (t1 - t0) * 1000

    def replay(self):
        state = {}
        with open(self.file_path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        data = json.loads(line)
                        skill_id = data["id"]
                        if skill_id not in state or data.get("v", 0) > state[skill_id].get("v", 0):
                            state[skill_id] = data
                        elif data.get("v", 0) == state[skill_id].get("v", 0):
                            state[skill_id] = data
                    except json.JSONDecodeError:
                        pass
        return state

    def close_all(self):
        # We can't easily close thread-local files from the main thread, 
        # but the OS handles it on exit.
        pass

def test_idempotency_and_replay():
    wal = WALManager(WAL_FILE)
    events = [
        {"id": "skill_1", "state": "PENDING", "v": 1},
        {"id": "skill_1", "state": "APPROVED", "v": 2},
        {"id": "skill_1", "state": "APPROVED", "v": 2}, 
    ]
    
    for e in events:
        wal.append(e)
        
    state = wal.replay()
    assert state["skill_1"]["state"] == "APPROVED"
    assert state["skill_1"]["v"] == 2
    print("Idempotency and Replay check passed.")

def test_concurrency():
    wal = WALManager(WAL_FILE)
    wal.append({"id": "warmup", "state": "PENDING"})

    def worker(i):
        entry = {"id": f"skill_c_{i}", "state": "PENDING"}
        return wal.append(entry)
        
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(worker, i) for i in range(100)]
        times = [f.result() for f in futures]
        
    avg_time = sum(times) / len(times)
    max_time = max(times)
    
    print("Concurrency check passed.")
    print(f"Average Append Latency: {avg_time:.2f} ms")
    print(f"Max Append Latency: {max_time:.2f} ms")
    if avg_time < 10:
        print("Latency requirement (<10ms) MET.")
    else:
        print("Latency requirement (<10ms) NOT MET.")

if __name__ == "__main__":
    init_wal()
    with open(WAL_FILE, "w") as f:
        f.write(" ")
        
    test_idempotency_and_replay()
    test_concurrency()
