#!/usr/bin/env python3
import cgi
import os
import json
import socket
import sys
import time
import secret
try:
    from cgi import escape #v3.7
except:
    from html import escape #v3.8

def login_page():
    """
    Returns the HTML for the login page.
    """

    return _wrapper(r"""
    <h1> Welcome! </h1>

    <form method="POST" action="hello.py">
        <label> <span>Username:</span> <input autofocus type="text" name="username"></label> <br>
        <label> <span>Password:</span> <input type="password" name="password"></label>

        <button type="submit"> Login! </button>
    </form>
    """)

def _wrapper(page):
    """
    Wraps some text in common HTML.
    """
    return ("""
    <!DOCTYPE HTML>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                max-width: 24em;
                margin: auto;
                color: #333;
                background-color: #fdfdfd
            }

            .spoilers {
                color: rgba(0,0,0,0); border-bottom: 1px dashed #ccc
            }
            .spoilers:hover {
                transition: color 250ms;
                color: rgba(36, 36, 36, 1)
            }

            label {
                display: flex;
                flex-direction: row;
            }

            label > span {
                flex: 0;
            }

            label> input {
                flex: 1;
            }

            button {
                font-size: larger;
                float: right;
                margin-top: 6px;
            }
        </style>
    </head>
    <body>
    """ + page + """
    </body>
    </html>
    """)

def secret_page(username=None, password=None):
    """
    Returns the HTML for the page visited after the user has logged-in.
    """
    if username is None or password is None:
        raise ValueError("You need to pass both username and password!")

    return _wrapper("""
    <h1> Welcome, {username}! </h1>

    <p> <small> Pst! I know your password is
        <span class="spoilers"> {password}</span>.
        </small>
    </p>
    """.format(username=escape(username.capitalize()),
               password=escape(password)))

def after_login_incorrect():
    """
    Returns the HTML for the page when the login credentials were typed
    incorrectly.
    """
    return _wrapper(r"""
    <h1> Login incorrect :c </h1>

    <p> Incorrect username or password (hint: <span class="spoilers"> Check
        <code>secret.py</code>!</span>)
    <p> <a href="hello.py"> Try again. </a>
    """)

def main():
    # code from the helper doc on eclass: https://eclass.srv.ualberta.ca/mod/page/view.php?id=5442506
    posted_bytes = os.environ.get("CONTENT_LENGTH", 0)
    if posted_bytes:
        posted = sys.stdin.read(int(posted_bytes))
        for line in posted.splitlines():
            l = line.split('&')
            if l[0].split('=')[1] == secret.username and l[1].split('=')[1] == secret.password:
                print('Set-Cookie: LoggedIn=true')
            
            print("Content-Type: text/html")
            print()
            # I realize how bad this is and wouldn't do this on a real project
            if 'HTTP_COOKIE' in os.environ and len(os.environ['HTTP_COOKIE']) > 0 and os.environ['HTTP_COOKIE'].split('=')[1].lower() == 'true':
                print(secret_page(username=l[0].split('=')[1], password=l[1].split('=')[1]))
            else:
                print(after_login_incorrect())
                
    else: 
        print("Content-Type: text/html")
        print()
        print(login_page())

main()


