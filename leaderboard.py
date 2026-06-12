from PIL import Image, ImageDraw

def test_leaderboard():
    img = Image.new("RGB", (1200, 800), (20, 20, 20))

    draw = ImageDraw.Draw(img)

    draw.text(
        (50, 50),
        "TOP RICHEST PLAYERS",
        fill=(255, 215, 0)
    )

    img.save("leaderboards/test.png")

    return "leaderboards/test.png"
