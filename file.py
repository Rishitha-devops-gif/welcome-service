import os
import platform
import time

def get_uptime():
    system = platform.system()
    if system == "Windows":
        # On Windows, use uptime from system boot time
        import ctypes
        from ctypes import wintypes, windll

        class SYSTEM_TIME(ctypes.Structure):
            _fields_ = [
                ("wYear", wintypes.WORD),
                ("wMonth", wintypes.WORD),
                ("wDayOfWeek", wintypes.WORD),
                ("wDay", wintypes.WORD),
                ("wHour", wintypes.WORD),
                ("wMinute", wintypes.WORD),
                ("wSecond", wintypes.WORD),
                ("wMilliseconds", wintypes.WORD),
            ]

        class SYSTEM_INFO(ctypes.Structure):
            _fields_ = [("dwOemId", wintypes.DWORD)]

        GetTickCount64 = windll.kernel32.GetTickCount64
        GetTickCount64.restype = ctypes.c_ulonglong
        milliseconds = GetTickCount64()
        seconds = int(milliseconds // 1000)
        return seconds

    elif system == "Linux":
        # On Linux, read /proc/uptime
        with open("/proc/uptime", "r") as f:
            uptime_seconds = float(f.readline().split()[0])
        return int(uptime_seconds)

    elif system == "Darwin":
        # On macOS, use sysctl to get kern.boottime
        import subprocess
        output = subprocess.check_output(["sysctl", "-n", "kern.boottime"]).decode()
        # Output is: { sec = 1688990000, usec = 0 } ...
        import re
        m = re.search(r"sec = (\d+)", output)
        if m:
            boot_time = int(m.group(1))
            uptime_seconds = int(time.time() - boot_time)
            return uptime_seconds
        else:
            raise RuntimeError("Could not parse kern.boottime")
    else:
        raise NotImplementedError(f"Unsupported system: {system}")

def format_uptime(seconds):
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days}d {hours}h {minutes}m {seconds}s"

if __name__ == "__main__":
    uptime_seconds = get_uptime()
    print("System Uptime:", format_uptime(uptime_seconds))
