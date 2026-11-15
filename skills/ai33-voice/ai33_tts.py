"""AI33 TTS helper: validate tags, list voices, generate speech.

Usage:
  python ai33_tts.py check FILE [--voice VOICE_ID]
  python ai33_tts.py voices --provider elevenlabs [--q TEXT] [--language Vietnamese] [--gender Female]
  python ai33_tts.py tts FILE --voice VOICE_ID [--speed 1] [--out DIR] [--script RAW.txt] [--task ID] [--model ID] [--force]

ElevenLabs voices run on eleven_v3 with its free-form audio tags ([sighs], [whispers], [curious]...).
Other providers keep the ai33 app tag list below. Tested 2026-11: clone voices run on MiniMax and ignore those tags.

API key: env var AI33_API_KEY.
"""
import argparse, json, os, re, shutil, sys, time, uuid, urllib.parse, urllib.request
from pathlib import Path

API = "https://api.ai33.pro"
UA = {"User-Agent": "Mozilla/5.0"}  # the API and its file host reject Python's default User-Agent (HTTP 403)

# Tags ai33 app offers in its tag menu (Higgs tags). Others are dropped as unverified.
TAGS = {
    # speed / pause
    "speed_very_slow", "speed_slow", "speed_fast", "speed_very_fast", "pause", "long_pause",
    # sound effects
    "cough", "laughter", "crying", "screaming", "burping", "humming", "sigh", "sniff", "sneeze",
    # emotions
    "affection", "amusement", "anger", "awe", "confusion", "contentment", "determination", "disgust",
    "elation", "enthusiasm", "fear", "longing", "pride", "relief", "sadness", "surprise",
    # delivery / voice
    "whispering", "shouting", "singing", "pitch_low", "pitch_high", "expressive_high", "expressive_low",
}
TAG_RE = re.compile(r"\[([^\[\]\n]+)\]")
BREAK_RE = re.compile(r"<break\b[^>]*>", re.I)
BREAK_OK = re.compile(r'<break time="(\d+(?:\.\d+)?)s"\s*/>')
TAG_PROVIDERS = {"elevenlabs", "minimax", "clone", "vbee", "fishaudio"}
V3_MODEL = "eleven_v3"
# ai33 app control tags that do nothing on eleven_v3 (it reads pace from punctuation and "…")
NOT_V3 = re.compile(r"speed_\w+|pitch_\w+|expressive_\w+|pause|long_pause")


def is_v3(voice):
    return (voice or "elevenlabs_").split("_", 1)[0] == "elevenlabs"


def check(text, v3=True):
    """Return (tag counts, list of problems). v3: free-form eleven_v3 tags; else the ai33 app list."""
    counts, problems = {}, []
    for m in TAG_RE.finditer(text):
        t = m.group(1).strip().lower()
        if v3 and NOT_V3.fullmatch(t):
            problems.append(f"[{m.group(1)}] at char {m.start()} has no effect on eleven_v3; use punctuation or …")
        elif v3 and len(t.split()) > 3:
            problems.append(f"tag [{m.group(1)}] at char {m.start()} too long; keep v3 tags to 1-3 words")
        elif v3 or t in TAGS:
            counts[t] = counts.get(t, 0) + 1
        else:
            problems.append(f"unknown tag [{m.group(1)}] at char {m.start()}")
    if v3 and BREAK_RE.search(text):
        problems.append("<break> is not supported on eleven_v3; use … or a new sentence")
    for m in BREAK_RE.finditer(text) if not v3 else ():
        ok = BREAK_OK.fullmatch(m.group(0))
        if not ok:
            problems.append(f"bad break syntax {m.group(0)!r}, use <break time=\"0.7s\"/>")
        elif not 0 < float(ok.group(1)) <= 3:
            problems.append(f"break {ok.group(1)}s outside 0-3s")
        else:
            counts["break"] = counts.get("break", 0) + 1
    return counts, problems


def clean_srt(srt):
    """Drop tags/breaks the transcript may echo, and cues left empty, so captions show only spoken words."""
    cues = []
    for block in re.split(r"\n\s*\n", srt.strip()):
        lines = block.strip().splitlines()
        if len(lines) < 2 or "-->" not in lines[1]:
            continue
        text = BREAK_RE.sub(" ", TAG_RE.sub(" ", "\n".join(lines[2:])))
        text = "\n".join(" ".join(l.split()) for l in text.splitlines() if l.strip())
        if text:
            cues.append(f"{len(cues) + 1}\n{lines[1].strip()}\n{text}")
    return "\n\n".join(cues) + "\n"


def key():
    k = os.environ.get("AI33_API_KEY")
    if not k and Path("AI33_KEY.txt").is_file():  # ai-animation-director keeps the key in this file
        k = Path("AI33_KEY.txt").read_text(encoding="utf-8-sig").split()[-1].strip("\"'")
    if not k:
        sys.exit("Missing env var AI33_API_KEY")
    return k


def call(method, path, fields=None):
    headers = {"xi-api-key": key(), **UA}
    body = None
    if fields is not None:
        boundary = uuid.uuid4().hex
        parts = [
            f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'
            for k, v in fields.items()
        ]
        body = ("".join(parts) + f"--{boundary}--\r\n").encode("utf-8")
        headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
    req = urllib.request.Request(API + path, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if method == "GET" and e.code in (429, 502, 503):  # polling busy; the task keeps running server-side
            return {"status": "busy"}
        sys.exit(f"HTTP {e.code} {path}: {e.read().decode('utf-8', 'replace')[:500]}")


def cmd_check(a):
    text = Path(a.file).read_text(encoding="utf-8")
    counts, problems = check(text, is_v3(a.voice))
    print(json.dumps({"chars": len(text), "tags": counts, "problems": problems}, ensure_ascii=False, indent=1))
    sys.exit(1 if problems else 0)


def cmd_voices(a):
    q = {"provider": a.provider, "page_size": a.limit}
    for k in ("q", "language", "gender"):
        if getattr(a, k):
            q[k] = getattr(a, k)
    res = call("GET", "/v3/voices?" + urllib.parse.urlencode(q))
    for v in res.get("data", []):
        print(f'{v["voice_id"]}\t{v.get("name","")}\t{v.get("language","")}\t{v.get("gender","")}')


def cmd_tts(a):
    text = Path(a.file).read_text(encoding="utf-8").strip()
    v3 = is_v3(a.voice)
    _, problems = check(text, v3)
    if problems and not a.force:
        sys.exit("Fix tags first (or --force):\n" + "\n".join(problems))
    provider = a.voice.split("_", 1)[0]
    if provider not in TAG_PROVIDERS and TAG_RE.search(text):
        print(f"warning: provider '{provider}' has no tag support in ai33 app; tags may be read aloud", file=sys.stderr)
    fields = {"text": text, "voice_id": a.voice, "speed": a.speed, "with_transcript": "true",
              "file_name": Path(a.file).stem}
    if a.model or v3:
        fields["model_id"] = a.model or V3_MODEL
    if a.dict:
        fields["pronunciation_dictionary_id"] = a.dict
    # --task: fetch a finished task again (e.g. after a failed download) without paying twice
    tid = a.task or call("POST", "/v3/text-to-speech", fields).get("task_id") or sys.exit("No task_id from /v3/text-to-speech")
    print("task", tid, file=sys.stderr)
    deadline = time.time() + a.timeout
    while True:
        t = call("GET", f"/v1/task/{tid}")
        if t["status"] == "done":
            break
        if t["status"] == "error":
            sys.exit(f"Task error: {t.get('error_message')}")
        if time.time() > deadline:
            sys.exit(f"Timeout; task {tid} still {t['status']} ({t.get('progress')}%)")
        time.sleep(4)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    stem = Path(a.file).stem.removesuffix(".tagged")  # x.tagged.txt -> x.mp3 / x.srt / x.txt
    meta = t.get("metadata") or {}
    saved = []
    for k in ("audio_url", "srt_url"):
        url = meta.get(k)
        if url:
            ext = Path(urllib.parse.urlparse(url).path).suffix or (".mp3" if k == "audio_url" else ".srt")
            dst = out / f"{stem}{ext}"
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
                dst.write_bytes(r.read())
            if ext == ".srt":
                dst.write_text(clean_srt(dst.read_text(encoding="utf-8-sig")), encoding="utf-8")
            saved.append(str(dst))
    if a.script:  # untagged script next to the audio, as make_video.py setup expects
        dst = out / f"{stem}.txt"
        if Path(a.script).resolve() != dst.resolve():
            shutil.copy2(a.script, dst)
        saved.append(str(dst))
    print(json.dumps({"task_id": tid, "credit_cost": t.get("credit_cost"), "files": saved}, indent=1))


def srt_time(sec):
    ms = round(sec * 1000)
    return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"


def shift_srt(srt, offset):
    def to_sec(ts):
        h, m, s = ts.replace(",", ".").split(":")
        return int(h) * 3600 + int(m) * 60 + float(s)
    return re.sub(r"(\d+:\d+:\d+,\d+) --> (\d+:\d+:\d+,\d+)",
                  lambda m: f"{srt_time(to_sec(m[1]) + offset)} --> {srt_time(to_sec(m[2]) + offset)}", srt)


def cmd_join(a):
    """Concatenate part mp3s (with a short silence between) and their .srt files, shifting each part's cues."""
    import subprocess
    parts = [Path(p) for p in a.parts]
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    dur = lambda f: float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                                         capture_output=True, text=True, check=True).stdout)
    cues, offset = [], 0.0
    for i, p in enumerate(parts):
        cues.append(shift_srt(clean_srt(p.with_suffix(".srt").read_text(encoding="utf-8-sig")), offset))
        offset += dur(p) + (a.gap if i < len(parts) - 1 else 0)
    srt = clean_srt("\n\n".join(cues))  # renumbers cues across parts
    out.with_suffix(".srt").write_text(srt, encoding="utf-8")
    ins = sum([["-i", str(p)] for p in parts], [])
    chain = "".join(f"[{i}:a]" + (f"apad=pad_dur={a.gap}" if i < len(parts) - 1 else "anull") + f"[a{i}];" for i in range(len(parts)))
    chain += "".join(f"[a{i}]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=0:a=1[out]"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", chain, "-map", "[out]", "-b:a", "192k", str(out)], check=True)
    print(json.dumps({"audio": str(out), "srt": str(out.with_suffix(".srt")), "seconds": round(dur(out), 2),
                      "srt_last_cue": next((l for l in reversed(srt.splitlines()) if "-->" in l), None)}, ensure_ascii=False, indent=1))


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check"); c.add_argument("file"); c.add_argument("--voice", help="voice id; elevenlabs (default) checks eleven_v3 tags")
    c.set_defaults(fn=cmd_check)
    v = sub.add_parser("voices"); v.add_argument("--provider", required=True)
    v.add_argument("--q"); v.add_argument("--language"); v.add_argument("--gender")
    v.add_argument("--limit", type=int, default=30); v.set_defaults(fn=cmd_voices)
    t = sub.add_parser("tts"); t.add_argument("file"); t.add_argument("--voice", required=True)
    t.add_argument("--speed", default="1"); t.add_argument("--out", default=".")
    t.add_argument("--dict"); t.add_argument("--force", action="store_true")
    t.add_argument("--model", help="override model_id (default eleven_v3 for elevenlabs voices)")
    t.add_argument("--task", help="reuse this finished task id instead of generating again")
    t.add_argument("--script", help="untagged script to copy beside the audio as <name>.txt")
    t.add_argument("--timeout", type=int, default=900); t.set_defaults(fn=cmd_tts)
    j = sub.add_parser("join", help="merge part mp3s + their .srt (long scripts generated in pieces)")
    j.add_argument("out", help="output .mp3; the .srt is written beside it"); j.add_argument("parts", nargs="+")
    j.add_argument("--gap", type=float, default=0.8, help="silence between parts, seconds"); j.set_defaults(fn=cmd_join)
    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
