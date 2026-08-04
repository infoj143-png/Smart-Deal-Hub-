# Script to generate premium high-resolution product images (Cover, Thumbnail, Social Preview) using PIL/Pillow.
import os
from PIL import Image, ImageDraw, ImageFont

def draw_circuits(draw, width, height, color):
    # Draw futuristic glowing circuit lines and nodes
    nodes = [
        (int(width * 0.1), int(height * 0.2)),
        (int(width * 0.25), int(height * 0.15)),
        (int(width * 0.15), int(height * 0.4)),
        (int(width * 0.85), int(height * 0.25)),
        (int(width * 0.75), int(height * 0.45)),
        (int(width * 0.9), int(height * 0.75)),
        (int(width * 0.2), int(height * 0.8)),
        (int(width * 0.35), int(height * 0.9)),
    ]

    # Draw connections
    for i in range(len(nodes) - 1):
        draw.line([nodes[i], nodes[i+1]], fill=color, width=2)

    # Draw circuit points
    for x, y in nodes:
        draw.ellipse([x-6, y-6, x+6, y+6], fill=color, outline="#FCD34D", width=2) # gold ring on nodes

def generate_cover_assets():
    # Style parameters
    W, H = 1000, 1500 # standard professional ratio for book cover

    # Base canvas
    base = Image.new("RGB", (W, H), "#0B0F19")
    draw = ImageDraw.Draw(base)

    # Render smooth vertical gradient
    for y in range(H):
        # Interpolate between dark blue (#0B0F19) and purple (#4C1D95)
        r = int(0x0B + (0x4C - 0x0B) * (y / H))
        g = int(0x0F + (0x1D - 0x0F) * (y / H))
        b = int(0x19 + (0x95 - 0x19) * (y / H))
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Draw futuristic elements
    draw_circuits(draw, W, H, "#7C3AED") # Glowing purple circuit lines

    font_title, font_sub, font_badge = None, None, None
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"
    ]

    for path in font_paths:
        if os.path.exists(path):
            try:
                font_title = ImageFont.truetype(path, 60)
                font_sub = ImageFont.truetype(path, 28)
                font_badge = ImageFont.truetype(path, 22)
                break
            except Exception:
                pass

    if not font_title:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_badge = ImageFont.load_default()

    # Draw Badge: "PDF * INSTANT DOWNLOAD" with gold accent
    badge_text = "PDF • INSTANT DOWNLOAD"
    draw.rectangle([W//2 - 200, 200, W//2 + 200, 260], fill="#7C3AED", outline="#FCD34D", width=2)
    draw.text((W//2, 230), badge_text, fill="#FFF", font=font_badge, anchor="mm")

    # Main Title
    title_lines = [
        "200 AI Prompts",
        "for Business Owners",
        "& Content Creators"
    ]

    current_y = 450
    for line in title_lines:
        draw.text((W//2, current_y), line, fill="#FFF", font=font_title, anchor="mm")
        current_y += 85

    # Gold divider line
    draw.line([(W//2 - 150, current_y + 40), (W//2 + 150, current_y + 40)], fill="#FCD34D", width=4)

    # Subtitle
    subtitle = "Save Time • Create Better Content • Grow Your Business with AI"
    draw.text((W//2, current_y + 120), subtitle, fill="#DDD6FE", font=font_sub, anchor="mm")

    # Draw simulated laptop displaying AI chat layout at the bottom
    laptop_y = 1050
    draw.rectangle([W//2 - 250, laptop_y, W//2 + 250, laptop_y + 280], fill="#1F2937", outline="#FCD34D", width=4) # screen outline
    draw.rectangle([W//2 - 230, laptop_y + 20, W//2 + 230, laptop_y + 240], fill="#0F172A") # screen display
    # chat bubbles on simulated screen
    draw.rectangle([W//2 - 210, laptop_y + 40, W//2 - 30, laptop_y + 100], fill="#374151") # prompt bubble
    draw.text((W//2 - 120, laptop_y + 70), "How can I automate my business?", fill="#9CA3AF", anchor="mm")

    draw.rectangle([W//2 - 30, laptop_y + 120, W//2 + 210, laptop_y + 220], fill="#7C3AED") # AI response bubble
    draw.text((W//2 + 90, laptop_y + 170), "Here are your 3 strategies...", fill="#FFF", anchor="mm")

    # Laptop keyboard base
    draw.rectangle([W//2 - 300, laptop_y + 280, W//2 + 300, laptop_y + 310], fill="#E5E7EB", outline="#9CA3AF", width=2)

    # Final watermark/footer branding
    draw.text((W//2, H - 100), "SMART DEAL HUB — PREMIUM SERIES", fill="#64748B", font=font_badge, anchor="mm")

    # Save cover
    os.makedirs("assets/images/ebooks", exist_ok=True)
    cover_path = "assets/images/ebooks/200-ai-prompts.jpg"
    base.save(cover_path, quality=90)
    print(f"Generated eBook cover image successfully: {cover_path}")

    # Create web product thumbnail by resizing cover
    thumb = base.resize((500, 750), Image.Resampling.LANCZOS)
    landscape = Image.new("RGB", (500, 312), "#0B0F19")
    landscape.paste(thumb.resize((208, 312), Image.Resampling.LANCZOS), (30, 0))
    ldraw = ImageDraw.Draw(landscape)
    ldraw.text((360, 100), "PREMIUM GUIDE", fill="#7C3AED", font=font_badge, anchor="mm")
    ldraw.text((360, 150), "200 AI PROMPTS", fill="#FFF", font=font_sub, anchor="mm")
    ldraw.text((360, 200), "PDF DOWNLOAD", fill="#FCD34D", font=font_badge, anchor="mm")

    landscape_path = "assets/images/ebooks/200-ai-prompts-landscape.jpg"
    landscape.save(landscape_path, quality=90)
    print(f"Generated landscape product image successfully: {landscape_path}")

if __name__ == "__main__":
    generate_cover_assets()
