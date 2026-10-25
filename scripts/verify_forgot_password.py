import urllib.request

def check(url, expected):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        content = resp.read().decode('utf-8')
        print(f"\n--- Testing {url} (Status: {resp.status}) ---")
        for exp in expected:
            found = exp.lower() in content.lower()
            print(f"  [ {'PASS' if found else 'FAIL'} ] Contains '{exp}'")

check('http://localhost:3000/login', ['Forgot password?', 'Sign In with Credentials'])
check('http://localhost:3000/forgot-password', ['Reset Password', 'Quick Fill Demo Account', 'Send Reset Instructions'])
check('http://localhost:3000/reset-password', ['Set New Password', 'New Password', 'Confirm New Password'])
