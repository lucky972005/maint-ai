with open(r'c:\dev\pro\app\api\chat\route.ts', 'r', encoding='utf-8') as f:
    content = f.read()

clean = (
    content.replace('\u2013', '-')
    .replace('\u2014', ' - ')
    .replace('\u2019', "'")
    .replace('\u201c', '"')
    .replace('\u201d', '"')
    .replace('\u00b1', '+/-')
    .replace('\u03bc', 'u')
    .replace('\u00b0C', '°C')
    .replace('\u03a9', 'Ω')
)

with open(r'c:\dev\pro\app\api\chat\route.ts', 'w', encoding='utf-8') as f:
    f.write(clean)

print('Standardized characters cleanly.')
