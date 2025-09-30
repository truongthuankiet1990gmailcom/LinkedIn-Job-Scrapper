import sys

# Fix encoding issues on Windows
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

print("[TEST] Testing encoding fix...")
print("[SUCCESS] No emojis, just text - this should work!")
print("[INFO] Script completed successfully")