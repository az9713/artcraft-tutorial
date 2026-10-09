"""Minimal MCP stdio client for the craft CLIs (newline-delimited JSON-RPC 2.0).

Usage as a library:
    from mcpclient import Craft
    with Craft([exe, "mcp", "--headless"]) as c:
        print(c.tools())
        r = c.call("run_command", {"id": "shape.rectangle", "params": {...}})
Usage as a script:  python mcpclient.py <exe> [args...]   -> prints the tool list
"""
import json
import subprocess
import sys


class Craft:
    def __init__(self, argv, cwd=None):
        self.p = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.DEVNULL, cwd=cwd, text=True,
                                  encoding="utf-8", bufsize=1)
        self.n = 0
        self.rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                                "clientInfo": {"name": "mcpclient", "version": "0"}})
        self._send({"jsonrpc": "2.0", "method": "notifications/initialized"})

    def _send(self, msg):
        self.p.stdin.write(json.dumps(msg) + "\n")
        self.p.stdin.flush()

    def rpc(self, method, params=None):
        self.n += 1
        self._send({"jsonrpc": "2.0", "id": self.n, "method": method, "params": params or {}})
        while True:
            line = self.p.stdout.readline()
            if not line:
                raise RuntimeError(f"server closed during {method}")
            msg = json.loads(line)
            if msg.get("id") == self.n:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg["result"]

    def tools(self):
        return self.rpc("tools/list")["tools"]

    def call(self, name, args=None):
        """Call a tool; return parsed JSON of the first text block when possible."""
        res = self.rpc("tools/call", {"name": name, "arguments": args or {}})
        texts = [b.get("text", "") for b in res.get("content", []) if b.get("type") == "text"]
        out = texts[0] if texts else res
        if isinstance(out, str):
            try:
                out = json.loads(out)
            except ValueError:
                pass
        if res.get("isError"):
            raise RuntimeError(f"{name} {json.dumps(args)[:300]} -> {out}")
        return out

    def close(self):
        try:
            self.p.stdin.close()
            self.p.wait(timeout=20)
        except Exception:
            self.p.kill()

    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.close()


if __name__ == "__main__":
    with Craft(sys.argv[1:]) as c:
        for t in c.tools():
            print(t["name"], "::", (t.get("description") or "")[:160].replace("\n", " "))
