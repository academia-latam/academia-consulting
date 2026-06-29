#!/usr/bin/env python3
"""
Generate AcademIA's engraving-style illustrations with Gemini
(gemini-2.5-flash-image). Modeled on ser-tutor/tools/generar_sprites_rpg.py.

Style: antique European copperplate/woodcut engraving, high-contrast black ink
on off-white. Bold, distinctive, anti-AI-slop. Output PNG + WebP.

USAGE
    1) Key in env or academia-consulting/.env:  GOOGLE_API_KEY=xxxx
       (we keep it global in ~/.config/secrets/ai.env)
    2) python tools/gen-images.py            # generate what's missing
       python tools/gen-images.py --only robot-bust
       python tools/gen-images.py --force

.env is gitignored; the key is never committed.
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

STYLE = (
    "Antique European copperplate engraving, fine cross-hatching and stipple line "
    "art, high-contrast BLACK ink on aged off-white paper, 18th-century scientific "
    "encyclopedia plate aesthetic, intricate detailed linework, strictly MONOCHROME "
    "(no color), no text, no letters, no numbers, no labels, no watermark, no "
    "signature, centered subject with clean negative space around it."
)

def plate(desc):
    return desc + ". Rendered as: " + STYLE

STAMP = ("Rough hand-printed rubber-stamp / letterpress ink emblem, visible ink "
         "texture with slightly broken irregular edges, bold solid BLACK ink on a "
         "PURE WHITE background, retro vintage postal-stamp aesthetic, simple and "
         "iconic, not busy, no gradients, no photo-realism, no grayscale shading.")
def stamp(desc):
    return desc + ". " + STAMP

# Clean LINOCUT system (approved art direction, see docs/superpowers/specs).
# Cohesive, hand-printed, NOT folk/busy, minimal faces to avoid the AI-uncanny look.
LINO = ("Bold CLEAN LINOCUT / woodblock print: thick, confident, EVEN-WEIGHT carved "
        "black lines, simple and elegant, with generous negative space and NOT busy. "
        "Any figures are simplified and stylized, with faces reduced to only a few "
        "confident lines (no detailed or realistic faces). NO fine cross-hatching, NO "
        "decorative folk borders, NO pattern noise, NO gray fills. Genuinely "
        "hand-printed look with slightly organic ink edges; NOT digital-smooth, NOT "
        "3D, NOT a photo. Strictly solid BLACK ink on a PURE WHITE background, very "
        "high contrast, centered with clean margins, no text, no letters, no numbers, "
        "no signature.")
def lino(desc):
    return desc + ". " + LINO

# name -> (prompt, (w,h), mode)  mode: square | wide | cover
MANIFEST = {
    "robot-bust": (plate(
        "A dignified humanoid robot bust, a brass-and-iron mechanical automaton head "
        "and shoulders with visible gears, rivets and lenses for eyes, calm and "
        "noble expression, facing forward like a museum specimen"),
        (900, 900), "cover"),
    "teacher-plate": (plate(
        "A teacher standing beside a chalkboard in front of a few attentive students "
        "at desks, a dignified classroom scene, the teacher in command of the room"),
        (1200, 800), "cover"),
    "hand-pen": (plate(
        "A human hand holding a dip pen, writing and marking corrections on a sheet "
        "of paper, close study of the hand and pen"),
        (760, 760), "cover"),
    "balance": (plate(
        "An old brass balance scale in equilibrium, classical emblem of judgment and "
        "ethics, on a plain plinth"),
        (760, 760), "cover"),
    "tool-tangle": (plate(
        "A cluttered desk overflowing with too many screens, gadgets, cables and "
        "tangled wires, chaotic pile of devices, overwhelming"),
        (1200, 800), "cover"),
    "owl-books": (plate(
        "An owl perched on a stack of old books, classical emblem of knowledge and "
        "teaching"),
        (760, 760), "cover"),
    "logo-a": (stamp(
        "A round postal ink stamp with a clean circular double-ring border; inside, "
        "the calm front-facing head of a friendly light steampunk robot automaton "
        "with a few rivets and a single small gear on the forehead; minimal and "
        "iconic; no text, no letters"), (1000, 1000), "cover"),
    "logo-b": (stamp(
        "The calm front-facing head of a friendly light steampunk robot automaton as "
        "a single bold ink emblem, a few rivets and one small gear, simple and "
        "iconic, centered, no frame, no text, no letters"), (1000, 1000), "cover"),
    "logo-c": (stamp(
        "A round official ink seal: a small robot automaton head in the center, with "
        "curved capital lettering around the outer ring reading ACADEMIA, a few tiny "
        "star dots, and a thin inner ring; vintage postal seal"), (1000, 1000), "cover"),
    "logo2-a": ("A robot head reimagined as a Mexican folk WOODCUT in the style of "
        "Jose Guadalupe Posada and Oaxacan linocut: hand-carved bold black ink lines, "
        "slightly naive, expressive, with decorative folk patterning. Solid black ink "
        "on a pure white background, rough hand-printed texture, high contrast, no "
        "gray shading, no gradients, iconic, centered, no text, no letters.",
        (1000, 1000), "cover"),
    "logo2-b": ("A friendly 1950s mid-century TIN-TOY robot head, boxy face with round "
        "dials and antennae, rendered as a bold LINOCUT block print: thick rough "
        "carved black ink lines, simple and charming. Solid black ink on a pure white "
        "background, high contrast, no gray, no gradients, iconic, centered, no text, "
        "no letters.", (1000, 1000), "cover"),
    "logo2-c": ("A minimal robot head drawn with a few confident SUMI-E brush strokes, "
        "Japanese ink-wash and hanko seal sensibility, abstract and gestural, rough "
        "brushed black ink. Solid black ink on a pure white background, high contrast, "
        "no gray, iconic, centered, no text, no letters.", (1000, 1000), "cover"),
    "logo3-s1": ("A robot head in a few BOLD confident SUMI-E brush strokes: thick "
        "gestural ink, minimal (simple head outline, two dot eyes, a short antenna), "
        "very high contrast, must read clearly at small size. Solid black ink on pure "
        "white, rough brushed edges, no gray, iconic, centered, no text.",
        (1000, 1000), "cover"),
    "logo3-s2": ("An enso (one bold SUMI-E brush ring) containing a minimal robot face: "
        "two dot eyes and a short mouth line. Thick confident brush, iconic, reads at "
        "small size. Solid black ink on pure white, rough brushed edges, no gray, "
        "centered, no text.", (1000, 1000), "cover"),
    "logo3-s3": ("An abstract AI spark in SUMI-E: a bold brushed central node with a few "
        "radiating brush strokes and connected dots, like a neuron or a seed of "
        "intelligence. Gestural, iconic, reads small. Solid black ink on pure white, "
        "rough brushed, no gray, centered, no text.", (1000, 1000), "cover"),
    "logo3-w1": ("A human BRAIN as a Mexican folk WOODCUT, with circuit traces and root "
        "patterns woven into the folds (intelligence meets machine), bold carved black "
        "ink lines, decorative, iconic, reads small. Solid black ink on pure white, "
        "rough printed, no gray, centered, no text.", (1000, 1000), "cover"),
    "logo3-w2": ("An OWL, emblem of wisdom and teaching, as a Mexican folk WOODCUT, with "
        "small gear and circuit motifs in its feathers, bold carved black ink lines, "
        "decorative folk patterning, iconic, reads small. Solid black ink on pure "
        "white, rough printed, no gray, centered, no text.", (1000, 1000), "cover"),
    "logo3-w3": ("A human HAND holding a glowing spark / node with small radiating "
        "lines (a person guiding the spark of AI), as a Mexican folk WOODCUT, bold "
        "carved black ink lines, decorative, iconic, reads small. Solid black ink on "
        "pure white, rough printed, no gray, centered, no text.", (1000, 1000), "cover"),
    "logo4-r2": ("A robot head in bold confident SUMI-E brush strokes, ROUNDER and "
        "friendlier head, two big dot eyes, one small antenna; thick gestural ink, very "
        "high contrast, reads clearly at small size. Solid black ink on pure white, "
        "rough brushed edges, no gray, centered, no text.", (1000, 1000), "cover"),
    "logo4-r3": ("A robot head as a bold square HANKO seal: a chunky brush-ink square "
        "frame with a minimal robot face inside (two eyes and a mouth slot); thick ink, "
        "reads at small size. Solid black ink on pure white, rough brushed printed "
        "edges, no gray, centered, no text.", (1000, 1000), "cover"),
    "logo4-h2": (lino(
        "Two cupped open hands from below holding a small glowing flame with a few "
        "short radiating lines above it (passing on the spark); simple and iconic"),
        (1000, 1000), "cover"),
    "logo4-h3": ("A single open hand, palm up, with a small radiant sun / node floating "
        "above it, Mexican folk WOODCUT, bold SIMPLE carved black ink lines, iconic, "
        "reads small. Solid black ink on pure white, rough printed, no gray, centered, "
        "no text.", (1000, 1000), "cover"),
    "logo4-n2": ("An AI neuron node in SUMI-E: a bold central ink dot with a FEW thick "
        "connecting strokes and three or four node dots (clean, few elements), reads at "
        "small size. Solid black ink on pure white, rough brushed, no gray, centered, "
        "no text.", (1000, 1000), "cover"),
    "logo4-n3": ("A sprouting seed of intelligence in SUMI-E: a node/seed with a small "
        "sprout and a couple of connection dots (learning growth plus AI), bold "
        "gestural ink, iconic, reads small. Solid black ink on pure white, rough "
        "brushed, no gray, centered, no text.", (1000, 1000), "cover"),
    "hero-spark": (lino(
        "A teacher gently passing a small glowing flame into the open cupped hands of a "
        "young student; the two simplified figures face each other, with a few simple "
        "radiant lines around the flame. Calm and graceful, plenty of negative space"),
        (1100, 1100), "cover"),
    "case-before": (lino(
        "One teacher at a desk surrounded by just a FEW too many floating app windows "
        "and small devices, two of them marked with a padlock or an expired-trial tag, "
        "and a couple of tangled cables; clearly overwhelmed but dignified. Keep it "
        "uncluttered and readable, only a few elements, lots of white space"),
        (900, 900), "cover"),
    "case-after": (lino(
        "The same teacher, now calm, reading a single open book with one attentive "
        "student beside her at a simple clear desk. Quiet and uncluttered"),
        (900, 900), "cover"),
    "icon-train": (lino(
        "A simple teacher figure with a pointer beside a small board, centered inside a "
        "thin rough circular stamp ring; minimal, iconic, reads tiny"), (420, 420), "cover"),
    "icon-redesign": (lino(
        "A single sheet of paper being reworked by a pencil, centered inside a thin "
        "rough circular stamp ring; minimal, iconic, reads tiny"), (420, 420), "cover"),
    "icon-equip": (lino(
        "Three small tool/app tiles with a checkmark (a curated toolkit), centered "
        "inside a thin rough circular stamp ring; minimal, iconic, reads tiny"),
        (420, 420), "cover"),
    "icon-govern": (lino(
        "A single blank sheet of paper with a small round wax seal at its lower corner "
        "(a signed policy), the whole thing centered inside a thin rough CIRCULAR stamp "
        "ring border; the paper is completely BLANK with absolutely no writing, letters "
        "or words anywhere; minimal, iconic, reads tiny"), (420, 420), "cover"),
    # logo5 — CIRCULAR STAMP marks engineered to stay legible at tiny sizes
    # (header 30px, favicon 32px). Bold, simple, very high contrast.
    "logo5-c1": ("A minimal robot face inside a single bold SUMI-E brush-ink CIRCLE "
        "(enso ring forming a stamp/seal); inside the ring a very simple robot: a "
        "rounded head, two big round dot eyes and one short antenna. Extremely bold "
        "and high-contrast so it stays legible at tiny sizes; thick confident brush, "
        "rough brushed ink edges, no fine detail, no gray. Solid BLACK ink on a PURE "
        "WHITE background, centered, no text, no letters, no numbers.",
        (1000, 1000), "cover"),
    "logo5-c2": ("A round rubber-stamp emblem with a bold DOUBLE-RING border and, "
        "inside it, the calm front-facing head of a simple friendly robot (rounded "
        "head, two big dot eyes, a small antenna). Hand-printed letterpress ink "
        "texture with slightly broken edges, very bold and iconic, reads clearly when "
        "tiny. Solid BLACK ink on a PURE WHITE background, no gradients, no gray "
        "shading, centered, no text, no letters, no numbers.",
        (1000, 1000), "cover"),
    "logo5-c3": ("A solid filled BLACK circular ink seal/disc with the simple robot "
        "rendered in NEGATIVE SPACE (cut out in white from the black disc): a rounded "
        "robot head with two eyes and a small antenna, plus a thin white inner ring. "
        "Bold rubber-stamp ink texture, extremely legible at tiny sizes. Flat BLACK "
        "disc on a PURE WHITE background, no gray, no gradient, centered, no text, no "
        "letters, no numbers.", (1000, 1000), "cover"),
    "logo5-c4": ("A simple friendly robot head inside a bold CLEAN LINOCUT circular "
        "medallion frame: a thick even-weight carved black ring; robot reduced to a "
        "rounded head with two dot eyes and a short antenna. Generous negative space, "
        "not busy, hand-printed woodblock texture, reads at tiny sizes. Solid BLACK "
        "ink on PURE WHITE, very high contrast, no gray, centered, no text, no "
        "letters, no numbers.", (1000, 1000), "cover"),
    "logo5-c5": ("A bold round HANKO seal: a thick brush-ink CIRCULAR ring with a "
        "minimal geometric robot face inside (a squarish head suggested by a few "
        "strokes, two eyes, one antenna). Chunky confident ink, rough printed edges, "
        "designed to read at very small sizes. Solid BLACK ink on a PURE WHITE "
        "background, no gray, centered, no text, no letters, no numbers.",
        (1000, 1000), "cover"),
    "logo5-c6": ("An ultra-simple robot head as a tiny-legible seal: a bold SUMI-E "
        "brush CIRCLE containing only a rounded robot head with two large dot eyes "
        "(no other detail at all). Maximum simplicity and contrast for legibility at "
        "16-32 pixels. Thick brush ink, rough edges, solid BLACK on PURE WHITE, "
        "centered, no text, no letters, no numbers.", (1000, 1000), "cover"),
    # logo6 — open HAND offering the spark, engraved with BANKNOTE / billete line texture
    "logo6-h1": ("An open human hand, palm up, gently offering a small radiant sun/star "
        "with pointed rays floating just above the palm (passing on the spark of "
        "knowledge). Rendered as a FINE STEEL-ENGRAVING in the style of CURRENCY / "
        "BANKNOTE engraving: the hand and arm modeled entirely with fine parallel "
        "hatched lines and contour line-shading (intaglio bank-note line work), like "
        "the portrait engraving on paper money. Crisp high-contrast BLACK ink lines on "
        "a PURE WHITE background, no solid fills, no gray wash, no photo, iconic, "
        "centered, no text, no letters, no numbers.", (1000, 1000), "cover"),
    "logo6-h2": ("An open hand, palm up, offering a small radiant star/sun above it. "
        "Engraved like a BANKNOTE: the form built from fine parallel burin lines and "
        "cross-hatching, and the sun's rays and the area around it filled with fine "
        "concentric GUILLOCHE bank-note line patterns. Old paper-money intaglio "
        "aesthetic. Crisp BLACK line engraving on a PURE WHITE background, very high "
        "contrast, no solid black fills, no gray, centered, no text, no letters, no "
        "numbers.", (1000, 1000), "cover"),
    "logo6-h3": ("An open hand holding up a small radiant sun, inside a thin oval "
        "BANK-NOTE medallion border of fine guilloche lines (like the framed portrait "
        "on a bill). The hand is modeled with fine engraved parallel hatching. Steel "
        "intaglio currency-engraving style, crisp BLACK lines on PURE WHITE, high "
        "contrast, no solid fills, no gray, centered, no text, no letters, no numbers.",
        (1000, 1000), "cover"),
    "logo6-h4": ("A single open hand, palm up, with a small radiant sun floating above "
        "it; clean and minimal but the hand SHADED with fine parallel engraved lines in "
        "the style of BANKNOTE / money steel-engraving. Confident line art, crisp BLACK "
        "ink lines on a PURE WHITE background, very high contrast, no solid fills, no "
        "gray, iconic, reads at small size, centered, no text, no letters, no numbers.",
        (1000, 1000), "cover"),
}

def get_key():
    k = os.environ.get("GOOGLE_API_KEY")
    if k:
        return k
    for p in [os.path.join(ROOT, ".env"), os.path.expanduser("~/.config/secrets/ai.env")]:
        if os.path.exists(p):
            for line in open(p):
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
    if mode in ("cover", "square"):
        img = ImageOps.fit(img, size, Image.LANCZOS)
    else:
        img.thumbnail(size, Image.LANCZOS)
    img.save(os.path.join(OUT, name + ".png"))
    img.save(os.path.join(OUT, name + ".webp"), "WEBP", quality=84, method=6)
    print(f"  saved assets/img/{name}.webp ({img.size[0]}x{img.size[1]})")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    key = get_key()
    if not key:
        print("ERROR: no GOOGLE_API_KEY (env or ~/.config/secrets/ai.env).")
        sys.exit(1)
    os.makedirs(OUT, exist_ok=True)
    jobs = [(n, *spec) for n, spec in MANIFEST.items() if not args.only or n in set(args.only)]
    done = 0
    for name, prompt, size, mode in jobs:
        webp = os.path.join(OUT, name + ".webp")
        if os.path.exists(webp) and not args.force:
            print(f"- {name}: exists (use --force)"); continue
        print(f"Generating {name} ...")
        raw = call_api(prompt, key)
        if raw:
            process_and_save(name, raw, size, mode); done += 1
    print(f"\nDone: {done} image(s) in assets/img/")

if __name__ == "__main__":
    main()
