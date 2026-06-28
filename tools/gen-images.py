#!/usr/bin/env python3
"""
Generate AcademIA's site illustrations with Gemini (nano-banana:
gemini-2.5-flash-image), at build time. Modeled on
/mnt/data/repos/ser-tutor/tools/generar_sprites_rpg.py.

Warm, human, editorial illustration style. Cohesive set: founder portraits,
hero background, a before/after story pair, and advantage spot illustrations.

USAGE
    1) Put your key in academia-consulting/.env (same key you already use):
           GOOGLE_API_KEY=xxxx
       (or:  export GOOGLE_API_KEY=xxxx)
    2) pip install requests pillow   (already present here)
    3) python tools/gen-images.py                 # generate what's missing
       python tools/gen-images.py --only hero-bg adv-time
       python tools/gen-images.py --force         # regenerate everything

The key is NEVER committed: .env is in .gitignore.
"""
import argparse, base64, io, os, sys
try:
    import requests
    from PIL import Image, ImageOps
except ImportError:
    print("ERROR: need 'requests' and 'pillow'  ->  pip install requests pillow")
    sys.exit(1)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img")
MODEL = "gemini-2.5-flash-image"
URL = "https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={k}"

# -------------------------------------------------------------- shared style
STYLE = (
    "Warm modern editorial illustration, friendly and human, optimistic but "
    "professional. Limited brand palette: deep azure blue as primary, a soft "
    "amber-gold accent, warm paper-white background, gentle soft shadows, subtle "
    "paper grain. Diverse Mexican teachers and students of varied ages and skin "
    "tones, respectful and authentic. Clean shapes with light painterly texture. "
    "Absolutely NO text, no letters, no words, no numbers, no UI, no logos, no "
    "watermark, no signature. Generous empty space for overlaid copy."
)

# Founder bases — illustrated (not real likeness), kept consistent.
GABY = ("a warm approachable Latina woman in her late 30s, shoulder-length dark "
        "wavy hair, genuine friendly smile, smart-casual blazer")
HESUS = ("a friendly Latino man in his early 30s, short dark hair, light groomed "
         "beard, modern glasses, genuine smile, casual collared shirt")
SERGIO = ("a thoughtful Latino man in his late 30s, short dark hair, glasses, "
          "warm smile, casual button-down shirt")

def portrait(base):
    return (f"Head-and-shoulders character portrait of {base}. Centered, facing "
            f"the viewer, confident and kind. Plain soft warm-neutral studio "
            f"background, even lighting, clean margin around the head so it can be "
            f"cropped to a circle. {STYLE}")

def scene(desc, wide=True):
    shape = "Wide 16:9 establishing illustration" if wide else "Square illustration"
    return f"{shape}: {desc}. {STYLE}"

# name -> (prompt, (w,h), mode)   mode: 'square' | 'wide' | 'cover'
MANIFEST = {
    "avatar-gaby":   (portrait(GABY),   (512, 512), "square"),
    "avatar-hesus":  (portrait(HESUS),  (512, 512), "square"),
    "avatar-sergio": (portrait(SERGIO), (512, 512), "square"),
    "hero-bg": (scene(
        "a bright Mexican university classroom where a teacher and a few students "
        "collaborate around laptops, with simple friendly abstract shapes floating "
        "to suggest ideas and AI; calm and hopeful, with large open negative space "
        "on the left third for a headline"), (1600, 1000), "cover"),
    "story-before": (scene(
        "one teacher alone at a desk late at night, stacks of paper and a single "
        "laptop, overwhelmed and tired, cooler muted tones", wide=False),
        (900, 900), "cover"),
    "story-after": (scene(
        "the same kind of teacher now confident and energized, guiding engaged "
        "diverse students, AI shown as small friendly helper shapes, warm bright "
        "tones", wide=False), (900, 900), "cover"),
    "adv-time": (scene(
        "a calm teacher reclaiming time, a soft clock motif and freed hands, "
        "relaxed", wide=False), (640, 640), "square"),
    "adv-feedback": (scene(
        "a teacher giving thoughtful personalized feedback to a few diverse "
        "students, attentive and fair", wide=False), (640, 640), "square"),
    "adv-responsible": (scene(
        "a teacher guiding students to use AI safely, a gentle shield and "
        "checkmark motif, trustworthy", wide=False), (640, 640), "square"),
    "adv-equity": (scene(
        "students of different backgrounds including rural and Indigenous, all "
        "included and reaching the same level together", wide=False),
        (640, 640), "square"),
    "og": (scene(
        "AcademIA key visual: warm editorial illustration of education meeting AI, "
        "a teacher and students with friendly abstract AI shapes, azure and amber, "
        "lots of clean space"), (1200, 630), "cover"),
}

def get_key():
    k = os.environ.get("GOOGLE_API_KEY")
    if k:
        return k
    env = os.path.join(ROOT, ".env")
    if os.path.exists(env):
        for line in open(env):
            if line.strip().startswith("GOOGLE_API_KEY="):
                return line.strip().split("=", 1)[1].strip().strip('"').strip("'")
    return None

def call_api(prompt, key):
    r = requests.post(
        URL.format(m=MODEL, k=key),
        json={"contents": [{"parts": [{"text": prompt}]}],
              "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}},
        headers={"Content-Type": "application/json"}, timeout=240)
    if r.status_code != 200:
        print(f"  ERROR {r.status_code}: {r.text[:300]}")
        return None
    for p in r.json().get("candidates", [{}])[0].get("content", {}).get("parts", []):
        if "inlineData" in p:
            return base64.b64decode(p["inlineData"]["data"])
    print("  ERROR: response had no image")
    return None

def process_and_save(name, raw, size, mode):
    img = Image.open(io.BytesIO(raw)).convert("RGB")
    if mode == "cover":
        img = ImageOps.fit(img, size, Image.LANCZOS)
    elif mode == "square":
        img = ImageOps.fit(img, size, Image.LANCZOS)
    else:  # wide: fit within keeping aspect
        img.thumbnail(size, Image.LANCZOS)
    png = os.path.join(OUT, name + ".png")
    webp = os.path.join(OUT, name + ".webp")
    img.save(png)
    img.save(webp, "WEBP", quality=82, method=6)
    print(f"  saved assets/img/{name}.webp ({img.size[0]}x{img.size[1]})")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    key = get_key()
    if not key:
        print("ERROR: no GOOGLE_API_KEY (put it in academia-consulting/.env or export it).")
        sys.exit(1)
    os.makedirs(OUT, exist_ok=True)
    jobs = [(n, *spec) for n, spec in MANIFEST.items()
            if not args.only or n in set(args.only)]
    done = 0
    for name, prompt, size, mode in jobs:
        webp = os.path.join(OUT, name + ".webp")
        if os.path.exists(webp) and not args.force:
            print(f"- {name}: exists (use --force)")
            continue
        print(f"Generating {name} ...")
        raw = call_api(prompt, key)
        if raw:
            process_and_save(name, raw, size, mode)
            done += 1
    print(f"\nDone: {done} image(s) in assets/img/")

if __name__ == "__main__":
    main()
