# draw_meme.py — builds the gta6-meme-x-01 variants (1024x1024) from AI base scenes.
# All captions are drawn here with PIL (crisp, correctly spelled) — never baked into
# the generated scene. The make.fun ghost is extracted ALONE from the official
# press-kit mark (mark-1024.png) and pasted as a character in the scene, with a
# soft contact shadow — never a corner sticker.
# Run: python3 draw_meme.py   (writes variants/*.png + 480px previews)

from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import numpy as np
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
OUT = os.path.join(HERE, "variants")
os.makedirs(OUT, exist_ok=True)

SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def text_center(d, cx, y, s, font, fill, stroke=0, stroke_fill=(0, 0, 0)):
    w = d.textlength(s, font=font)
    d.text((cx - w / 2, y), s, font=font, fill=fill,
           stroke_width=stroke, stroke_fill=stroke_fill)
    return y + font.size


def square_crop(im):
    """Centre-crop a 1920x1280 scene to a 1280x1280 square, then 1024."""
    w, h = im.size
    side = h
    x0 = (w - side) // 2
    return im.crop((x0, 0, x0 + side, side)).resize((1024, 1024), Image.LANCZOS)


def ghost_alone():
    """Extract the white ghost + its magenta star coin ALONE from the press-kit
    mark (drop the magenta disc and the outer black ring). Returns RGBA."""
    mark = Image.open(os.path.join(ASSETS, "ghost-mark.png")).convert("RGBA")
    rgb = np.asarray(mark.convert("RGB")).astype(int)
    alpha = np.asarray(mark.split()[3])
    h, w, _ = rgb.shape
    yy, xx = np.mgrid[0:h, 0:w]
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    white = (r > 230) & (g > 230) & (b > 230)
    black = (r < 60) & (g < 60) & (b < 60)
    dist_c = np.sqrt((xx - 512) ** 2 + (yy - 512) ** 2)
    dist_coin = np.sqrt((xx - 766) ** 2 + (yy - 432) ** 2)
    mask = ((dist_c < 400) & (white | black)) | (dist_coin < 122)
    mask = mask & (alpha > 0)
    m = Image.fromarray((mask * 255).astype(np.uint8), "L")
    m = m.filter(ImageFilter.GaussianBlur(1.5))
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.paste(mark, (0, 0), m)
    bbox = out.getbbox()
    return out.crop(bbox)


def paste_ghost(base, ghost, cx, top, width):
    """Paste ghost centred at cx, top edge at `top`, with a soft shadow."""
    gh = ghost.resize((width, int(ghost.size[1] * width / ghost.size[0])),
                      Image.LANCZOS)
    x0 = int(cx - gh.size[0] / 2)
    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    sh = Image.new("RGBA", gh.size, (0, 0, 0, 0))
    sh.putalpha(gh.split()[3].point(lambda a: int(a * 0.45)))
    shadow.paste(sh, (x0 + 10, top + 12), sh)
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    base.alpha_composite(shadow)
    base.alpha_composite(gh, (x0, top))
    return top + gh.size[1]


def wasted(subline, name):
    scene = Image.open(os.path.join(
        ASSETS, "media-generation-wasted-scene-0-49131c8e-57bc-437d-9864-cf9f53678886.png")).convert("RGB")
    img = square_crop(scene)
    img = ImageEnhance.Color(img).enhance(0.55)
    img = ImageEnhance.Brightness(img).enhance(0.92)
    img = img.convert("RGBA")
    d = ImageDraw.Draw(img)
    # top shade so WASTED reads over the sky
    shade = Image.new("RGBA", (1024, 330), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    for i in range(330):
        sd.line([(0, i), (1024, i)], fill=(0, 0, 0, int(110 * (1 - i / 330))))
    img.alpha_composite(shade)
    d = ImageDraw.Draw(img)
    text_center(d, 512, 55, "WASTED", F(SANS_B, 168), (208, 208, 208), 6)
    text_center(d, 512, 245, subline, F(SANS_B, 42), (255, 255, 255), 3)
    ghost = ghost_alone()
    bottom = paste_ghost(img, ghost, 512, 380, 300)
    d = ImageDraw.Draw(img)
    text_center(d, 512, bottom + 12, "make.fun", F(SANS_B, 34),
                (255, 255, 255), 3)
    img.convert("RGB").save(os.path.join(OUT, name), quality=95)
    img.convert("RGB").resize((480, 480), Image.LANCZOS).save(
        os.path.join(OUT, name.replace(".png", "-480.png")), quality=92)


def wanted(name):
    scene = Image.open(os.path.join(
        ASSETS, "media-generation-wanted-board-0-996ece73-aa0e-4704-9468-c8e3a4ea076d.png")).convert("RGB")
    img = square_crop(scene).convert("RGBA")
    d = ImageDraw.Draw(img)
    ink = (43, 33, 22)
    # poster text on the blank pinned sheet (sheet spans ~x0-984, y~208-904)
    text_center(d, 492, 250, "WANTED", F(SERIF_B, 118), ink)
    d.line([(272, 395), (712, 395)], fill=ink, width=4)
    text_center(d, 492, 425, "ROCKSTAR GAMES", F(SERIF_B, 56), ink)
    text_center(d, 492, 505, "FOR MAKING US WAIT", F(SANS_B, 40), ink)
    text_center(d, 492, 560, "13 YEARS", F(SANS_B, 66), ink)
    text_center(d, 492, 660, "REWARD: ONE VERY PATIENT", F(SANS_B, 32), ink)
    text_center(d, 492, 700, "FANBASE", F(SANS_B, 32), ink)
    ghost = ghost_alone()
    paste_ghost(img, ghost, 900, 85, 230)
    d = ImageDraw.Draw(img)
    text_center(d, 900, 292, "make.fun", F(SANS_B, 30), (255, 255, 255), 3)
    img.convert("RGB").save(os.path.join(OUT, name), quality=95)
    img.convert("RGB").resize((480, 480), Image.LANCZOS).save(
        os.path.join(OUT, name.replace(".png", "-480.png")), quality=92)


def wasted_v3(name):
    """A2-fixed: A2 caption + 'GTA 6' in-image, ghost lowered to hover over the
    fallen player as the extra life: revive beam, ground glow, '+1' cue."""
    scene = Image.open(os.path.join(
        ASSETS, "media-generation-wasted-scene-0-49131c8e-57bc-437d-9864-cf9f53678886.png")).convert("RGB")
    img = square_crop(scene)
    img = ImageEnhance.Color(img).enhance(0.55)
    img = ImageEnhance.Brightness(img).enhance(0.92)
    img = img.convert("RGBA")
    d = ImageDraw.Draw(img)
    shade = Image.new("RGBA", (1024, 330), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    for i in range(330):
        sd.line([(0, i), (1024, i)], fill=(0, 0, 0, int(110 * (1 - i / 330))))
    img.alpha_composite(shade)
    d = ImageDraw.Draw(img)
    text_center(d, 512, 55, "WASTED", F(SANS_B, 168), (208, 208, 208), 6)
    text_center(d, 512, 245, "13 YEARS WAITING FOR GTA 6. 0 REGRETS.",
                F(SANS_B, 36), (255, 255, 255), 3)
    ghost = ghost_alone()
    # revive beam: soft magenta column from ghost down toward the body
    beam = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    bd = ImageDraw.Draw(beam)
    for y in range(700, 870):
        a = int(46 * (1 - (y - 700) / 170))
        bd.line([(452, y), (572, y)], fill=(214, 38, 140, a))
    beam = beam.filter(ImageFilter.GaussianBlur(14))
    img.alpha_composite(beam)
    # ground glow where the revive light hits the wet street
    glow = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([332, 838, 692, 892], fill=(214, 38, 140, 70))
    glow = glow.filter(ImageFilter.GaussianBlur(16))
    img.alpha_composite(glow)
    bottom = paste_ghost(img, ghost, 512, 470, 300)
    d = ImageDraw.Draw(img)
    # '+1' extra-life cue by the ghost's star coin (coin sits upper-right)
    text_center(d, 668, 492, "+1", F(SANS_B, 46), (235, 60, 160), 3,
                stroke_fill=(255, 255, 255))
    text_center(d, 512, bottom + 12, "make.fun", F(SANS_B, 34),
                (255, 255, 255), 3)
    img.convert("RGB").save(os.path.join(OUT, name), quality=95)
    img.convert("RGB").resize((480, 480), Image.LANCZOS).save(
        os.path.join(OUT, name.replace(".png", "-480.png")), quality=92)


def wasted_v4(name):
    """A4 (fix round): A3 caption shortened to '13 YEARS FOR GTA 6. WORTH IT.'
    rendered bigger (48px), and the revive beam rebuilt so it is ACTUALLY
    visible: the A3 beam (alpha<=46, drawn BEFORE the ghost, blurred 14)
    was invisible in the 480px view — parent verified no beam at all.
    A4 draws a 3-layer magenta beam AFTER the ghost paste, from the star
    coin (608,564) down to the fallen player's torso (555,845), plus a
    coin halo and a strong ground glow. Beam is drawn before the wordmark
    so 'make.fun' stays legible on top of it."""
    scene = Image.open(os.path.join(
        ASSETS, "media-generation-wasted-scene-0-49131c8e-57bc-437d-9864-cf9f53678886.png")).convert("RGB")
    img = square_crop(scene)
    img = ImageEnhance.Color(img).enhance(0.55)
    img = ImageEnhance.Brightness(img).enhance(0.92)
    img = img.convert("RGBA")
    d = ImageDraw.Draw(img)
    shade = Image.new("RGBA", (1024, 330), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    for i in range(330):
        sd.line([(0, i), (1024, i)], fill=(0, 0, 0, int(110 * (1 - i / 330))))
    img.alpha_composite(shade)
    d = ImageDraw.Draw(img)
    text_center(d, 512, 55, "WASTED", F(SANS_B, 168), (208, 208, 208), 6)
    text_center(d, 512, 240, "13 YEARS FOR GTA 6. WORTH IT.",
                F(SANS_B, 48), (255, 255, 255), 3)
    ghost = ghost_alone()
    bottom = paste_ghost(img, ghost, 512, 470, 300)
    # --- revive beam, drawn AFTER the ghost so nothing hides it ---
    # coin centre (608,564) measured from the pasted ghost; beam runs from
    # the coin's bottom edge to the fallen player's torso (555,845).
    MAG = (214, 38, 140)
    beam = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    bd = ImageDraw.Draw(beam)

    def taper_poly(x0, y0, x1, y1, w0, w1):
        dx, dy = x1 - x0, y1 - y0
        L = (dx * dx + dy * dy) ** 0.5
        nx, ny = -dy / L * 0.5, dx / L * 0.5
        return [(x0 + nx * w0, y0 + ny * w0), (x0 - nx * w0, y0 - ny * w0),
                (x1 - nx * w1, y1 - ny * w1), (x1 + nx * w1, y1 + ny * w1)]

    bd.polygon(taper_poly(608, 600, 555, 845, 96, 54), fill=MAG + (105,))
    beam = beam.filter(ImageFilter.GaussianBlur(16))
    img.alpha_composite(beam)
    beam2 = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    bd2 = ImageDraw.Draw(beam2)
    bd2.polygon(taper_poly(608, 600, 555, 845, 46, 26), fill=MAG + (190,))
    beam2 = beam2.filter(ImageFilter.GaussianBlur(7))
    img.alpha_composite(beam2)
    beam3 = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    bd3 = ImageDraw.Draw(beam3)
    bd3.polygon(taper_poly(608, 600, 555, 845, 15, 9), fill=(255, 90, 190, 235))
    bd3.line([(608, 600), (555, 845)], fill=(255, 255, 255, 150), width=5)
    beam3 = beam3.filter(ImageFilter.GaussianBlur(3))
    img.alpha_composite(beam3)
    # coin halo: light bursting out of the star coin
    halo = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    hd = ImageDraw.Draw(halo)
    for r, a in ((110, 55), (75, 95), (48, 140)):
        hd.ellipse([608 - r, 564 - r, 608 + r, 564 + r], fill=MAG + (a,))
    halo = halo.filter(ImageFilter.GaussianBlur(12))
    img.alpha_composite(halo)
    # ground glow where the revive light lands on the wet street
    glow = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([320, 818, 800, 892], fill=MAG + (150,))
    gd.ellipse([420, 832, 700, 882], fill=(255, 90, 190, 190))
    glow = glow.filter(ImageFilter.GaussianBlur(18))
    img.alpha_composite(glow)
    # sparkles riding the beam down to the body
    sp = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    spd = ImageDraw.Draw(sp)
    for cx, cy, r in ((596, 668, 13), (578, 742, 10), (564, 806, 12)):
        spd.polygon([(cx, cy - r), (cx + r * 0.28, cy - r * 0.28),
                     (cx + r, cy), (cx + r * 0.28, cy + r * 0.28),
                     (cx, cy + r), (cx - r * 0.28, cy + r * 0.28),
                     (cx - r, cy), (cx - r * 0.28, cy - r * 0.28)],
                    fill=(255, 255, 255, 230))
    sp = sp.filter(ImageFilter.GaussianBlur(1))
    img.alpha_composite(sp)
    d = ImageDraw.Draw(img)
    # '+1' extra-life cue by the ghost's star coin
    text_center(d, 668, 492, "+1", F(SANS_B, 46), (235, 60, 160), 3,
                stroke_fill=(255, 255, 255))
    text_center(d, 512, bottom + 12, "make.fun", F(SANS_B, 34),
                (255, 255, 255), 3)
    img.convert("RGB").save(os.path.join(OUT, name), quality=95)
    img.convert("RGB").resize((480, 480), Image.LANCZOS).save(
        os.path.join(OUT, name.replace(".png", "-480.png")), quality=92)


if __name__ == "__main__":
    wasted("13 YEARS WAITING. STILL WORTH IT.", "a1-wasted.png")
    wasted("13 YEARS. 0 REGRETS.", "a2-wasted-0regrets.png")
    wanted("b-wanted.png")
    wasted_v3("a3-wasted-fixed.png")
    wasted_v4("a4-wasted-revive.png")
    print("done:", sorted(os.listdir(OUT)))
