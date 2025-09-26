import asyncio
import re
import platform
import aiosqlite

DOMAINS = ["google.com", "facebook.com"]
MAX_HOPS = 3
TRACEROUTE_CMD = "tracert" if platform.system() == "Windows" else f"traceroute -m {MAX_HOPS}"
DB_FILE = "traceroute.db"

async def save_hops(domain, hops):
    async with aiosqlite.connect(DB_FILE) as db:
        for hop_num, ip, latency in hops:
            await db.execute(
                "INSERT INTO traceroute_results (domain, hop_num, hop_ip, latency) VALUES (?, ?, ?, ?)",
                (domain, hop_num, ip, latency)
            )
        await db.commit()
    print(f"✅ Saved {len(hops)} hops for {domain} to database.")

async def run_traceroute(domain):
    print(f"\nRunning traceroute for: {domain}")
    
    proc = await asyncio.create_subprocess_shell(
        f"{TRACEROUTE_CMD} {domain}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    hops = []
    hop_count = 0

    while True:
        line = await proc.stdout.readline()
        if not line:
            break
        decoded = line.decode().strip()
        print(decoded)

        # Parse hop IP + latency (Linux style)
        match = re.search(r"(\d+)\s+.*?(\d+\.\d+\.\d+\.\d+).*?(\d+\.\d+)\s+ms", decoded)
        if match:
            hop_num, ip, latency = match.groups()
            hops.append((int(hop_num), ip, float(latency)))
            hop_count += 1

        if hop_count >= MAX_HOPS:
            print("✅ Max hops reached, stopping traceroute.")
            proc.terminate()
            break

    await proc.wait()
    print(f"✅ Traceroute for {domain} finished. Total hops recorded: {len(hops)}")
    await save_hops(domain, hops)  # Save to DB

async def main():
    await asyncio.gather(*(run_traceroute(d) for d in DOMAINS))

asyncio.run(main())