import asyncio
import datetime
import time
import subprocess
import sys

# Peak hour range (Local / WIB timezone)
START_HOUR = 8
END_HOUR = 23

# Running flag
IS_RUNNING = True

def is_peak_hour():
    """Check if the current local time is within peak hours."""
    now = datetime.datetime.now()
    return START_HOUR <= now.hour < END_HOUR

async def main():
    print("====================================================")
    print("    🌐 WEBSITE TRAFFIC SCHEDULER ACTIVE             ")
    print(f"    Peak Hours: {START_HOUR:02d}:00 - {END_HOUR:02d}:00 Local Time")
    print("====================================================")
    
    # Calculate how many sessions to generate per block
    # Target is ~300 sessions per day over 15 hours -> ~20 sessions per hour.
    # We will run a loop of small batches to allow easy pausing and checking.
    
    while IS_RUNNING:
        now = datetime.datetime.now()
        
        if is_peak_hour():
            print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] Peak hours active. Launching traffic generation batch...")
            
            # Start run_traffic.py with CLI override for a small batch (e.g. 20 sessions)
            # This ensures we don't start a huge 900-session task that can't be safely paused.
            # Concurrency is set in config.yaml (5 concurrent).
            process = await asyncio.create_subprocess_exec(
                sys.executable, "run_traffic.py", "--sessions", "20",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Batch of 20 sessions completed successfully.")
            else:
                print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error in batch execution: {stderr.decode()}")
            
            # Wait for 10-15 minutes before launching the next batch to distribute traffic naturally
            sleep_time = 600 # 10 minutes
            print(f"Sleeping for {sleep_time} seconds before next batch...")
            await asyncio.sleep(sleep_time)
            
        else:
            # It's night time. Calculate sleep duration until 8:00 AM next day.
            current_time = datetime.datetime.now()
            target_time = current_time.replace(hour=START_HOUR, minute=0, second=0, microsecond=0)
            
            if current_time.hour >= END_HOUR:
                # If it is past 23:00, target is 8:00 AM tomorrow
                target_time += datetime.timedelta(days=1)
                
            sleep_duration = (target_time - current_time).total_seconds()
            
            print(f"[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] Night time (Off-peak). Pausing traffic generation.")
            print(f"Sleeping for {sleep_duration/3600:.2f} hours until {target_time.strftime('%Y-%m-%d %H:%M:%S')}...")
            
            await asyncio.sleep(sleep_duration)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nScheduler stopped by user.")
        sys.exit(0)
