# ProxyChecker (HTTP)

😈 A simple and efficient HTTP proxy checker tool  
☠️ **Made by MoonRise Network**

## Usage

Run the proxy checker with the following command:

```bash
python checker.py -i proxies.txt -o checked.txt -t 100 --timeout 5
```

## Available Arguments

- `-i/--input`: Input file containing proxies (default: `proxies.txt`)
- `-o/--output`: Output file for working proxies (default: `checked.txt`)
- `-t/--threads`: Number of threads (default: `50`)
- `--timeout`: Connection timeout in seconds (default: `10`)

## Help

To view the help message:

```bash
python checker.py --help
```
