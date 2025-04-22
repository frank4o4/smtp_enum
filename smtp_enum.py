# Copy of smtp-user-enum just converted it to python3
# Orginal Author https://pentestmonkey.net/tools/user-enumeration/smtp-user-enum
#

import smtplib
import argparse
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

def check_user(host, port, user, mode, from_addr, domain, timeout):
    try:
        username = f"{user}@{domain}" if domain else user
        with smtplib.SMTP(host, port, timeout=timeout) as server:
            server.ehlo()

            if mode == "VRFY":
                code, response = server.verify(username)
            elif mode == "EXPN":
                code, response = server.docmd("EXPN", username)
            elif mode == "RCPT":
                server.mail(from_addr)
                code, response = server.rcpt(username)
            else:
                return (host, user, "invalid mode")

            if code >= 500:
                return (host, username, "no such user")
            elif code >= 200 and code < 300:
                return (host, username, "exists")
            else:
                return (host, username, response.decode())
    except socket.timeout:
        return (host, user, "timeout")
    except Exception as e:
        return (host, user, f"error: {e}")

def load_file(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip()]

def main():
    parser = argparse.ArgumentParser(description="SMTP user enumeration tool")
    parser.add_argument("-u", help="Single username")
    parser.add_argument("-U", help="File with usernames")
    parser.add_argument("-t", help="Single host")
    parser.add_argument("-T", help="File with hosts")
    parser.add_argument("-m", type=int, default=5, help="Max parallel threads (default: 5)")
    parser.add_argument("-M", choices=["VRFY", "EXPN", "RCPT"], default="VRFY", help="SMTP command to use")
    parser.add_argument("-f", default="user@example.com", help="MAIL FROM address (for RCPT mode)")
    parser.add_argument("-D", help="Append domain to usernames")
    parser.add_argument("-p", type=int, default=25, help="SMTP port (default: 25)")
    parser.add_argument("-d", action="store_true", help="Debug mode")
    parser.add_argument("-v", action="store_true", help="Verbose")
    parser.add_argument("--timeout", type=int, default=5, help="Timeout in seconds (default: 5)")

    args = parser.parse_args()

    if not (args.u or args.U) or not (args.t or args.T):
        parser.error("Must provide at least one username (-u or -U) and one host (-t or -T)")

    usernames = [args.u] if args.u else load_file(args.U)
    hosts = [args.t] if args.t else load_file(args.T)

    print(f"\n### Starting SMTP User Enumeration (Mode: {args.M}) ###")
    print(f"Total usernames: {len(usernames)} | Hosts: {len(hosts)} | Threads: {args.m}")
    print(f"Start time: {datetime.now()}\n")

    results = []
    with ThreadPoolExecutor(max_workers=args.m) as executor:
        futures = {
            executor.submit(check_user, host, args.p, user, args.M, args.f, args.D, args.timeout): (host, user)
            for host in hosts for user in usernames
        }
        for future in as_completed(futures):
            host, user = futures[future]
            try:
                result = future.result()
                if args.v or result[2] != "no such user":
                    print(f"{result[0]}: {result[1]} => {result[2]}")
            except Exception as exc:
                print(f"{host}: {user} generated an exception: {exc}")

    print(f"\n### Finished at {datetime.now()} ###")

if __name__ == "__main__":
    main()
