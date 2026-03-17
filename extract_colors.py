try:
    from PIL import Image
    from collections import Counter
    img = Image.open('Vanille Asset Handout/vanille main logo maroon and cream-01.png').convert('RGBA')
    pixels = img.getdata()
    # Filter transparent pixels out
    solid_pixels = [p[:3] for p in pixels if p[3] > 200]
    counts = Counter(solid_pixels)
    print("Most common colors:")
    # Ignore absolute whites and blacks if they just padding
    filtered = []
    for color, count in counts.most_common(50):
        if color == (255,255,255) or color == (0,0,0) or color == (254,254,254) or color == (1,1,1):
            continue
        filtered.append((color, count))
    
    for color, count in filtered[:5]:
        print(f'Color: #{color[0]:02x}{color[1]:02x}{color[2]:02x}, Count: {count}')
except ImportError:
    print('Pillow not installed')
except Exception as e:
    print('Error:', e)
