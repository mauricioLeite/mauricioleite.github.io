#!/usr/bin/env python3

import sys
import subprocess
from datetime import datetime
import re
from pathlib import Path
import textwrap

# Colors
GREEN = '\033[0;92m'
RED = '\033[0;31m'
NC = '\033[0m'
SERVICE_NAME = "mauricioferreira-blog"

def print_message(msg):
    print(f"{GREEN}[INFO]{NC} {msg}")


def print_error(err):
    print(f"{RED}[ERROR]{NC} {err}", file=sys.stderr)

def start_dev():
    print_message("Starting environmnet...")
    subprocess.run(['docker', 'compose', 'up', '-d'], check=True)
    print_message("Server: http://localhost:1313")

def stop_dev():
    print_message("Stopping environmnet...")
    subprocess.run(['docker', 'compose', 'down'], check=True)

def rebuild():
    print_message("Rebuilding...")
    subprocess.run(['docker', 'compose', 'down'], check=True)
    subprocess.run(['docker', 'compose', 'build', '--no-cache'], check=True)
    subprocess.run(['docker', 'compose', 'up', '-d'], check=True)

def logs():
    subprocess.run(['docker', 'compose', 'logs', '-f'])

def new_post(title):
    if not title:
        print_error("Title not specified!")
        sys.exit(1)
    
    title = ' '.join(title)
    now = datetime.now()

    base_path = now.strftime('%Y/%m/%d')
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    new_dir = Path(f"content/{base_path}/{slug}")

    print_message(f"Creating post: {new_dir}")

    new_dir.mkdir(parents=True, exist_ok=True)

    body = textwrap.dedent(f"""\
        ---
        title: "{title}"
        slug: "{slug}"
        date: {now.strftime('%Y-%m-%dT%H:%M:%S%z')}
        draft: false
        description: "Post description here"
        tags: []
        categories: []
        ---

        Post content here...
        """)

    index = new_dir / "index.md"
    index.write_text(body, encoding='utf-8')

    print_message(f"New post created at {index}")


def show_help():
    help_text = """Commands:
  start            - Starts the environment
  stop             - Stops the environment
  restart          - Restarts the environment
  rebuild          - Rebuilds the image
  logs             - Shows the logs
  new-post <title> - Creates a new post
  help             - Shows this help message"""
    print(help_text)


def main():
    if len(sys.argv) < 2:
        command = 'help'
        args = []
    else:
        command = sys.argv[1]
        args = sys.argv[2:]

    commands = {
        'start': lambda: start_dev(),
        'stop': lambda: stop_dev(),
        'restart': lambda: (stop_dev(), start_dev()),
        'rebuild': lambda: rebuild(),
        'logs': lambda: logs(),
        'new-post': lambda: new_post(args),
        'help': lambda: show_help(),
        '--help': lambda: show_help(),
        '-h': lambda: show_help(),
    }

    if command in commands:
        try:
            commands[command]()
        except subprocess.CalledProcessError as e:
            print_error(f"Command failed with code {e.returncode}")
            sys.exit(1)
        except KeyboardInterrupt:
            print("\nUser Interrupt")
            sys.exit(130)
    else:
        print_error(f"Unknown command: {command}")
        show_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
    
