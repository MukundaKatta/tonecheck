"""CLI for tonecheck."""
import sys, json, argparse
from .core import Tonecheck

def main():
    parser = argparse.ArgumentParser(description="ToneCheck — Email Tone Detector. Analyze email tone before sending to avoid miscommunication.")
    parser.add_argument("command", nargs="?", default="status", choices=["status", "run", "info"])
    parser.add_argument("--input", "-i", default="")
    args = parser.parse_args()
    instance = Tonecheck()
    if args.command == "status":
        print(json.dumps(instance.get_stats(), indent=2))
    elif args.command == "run":
        print(json.dumps(instance.detect(input=args.input or "test"), indent=2, default=str))
    elif args.command == "info":
        print(f"tonecheck v0.1.0 — ToneCheck — Email Tone Detector. Analyze email tone before sending to avoid miscommunication.")

if __name__ == "__main__":
    main()
