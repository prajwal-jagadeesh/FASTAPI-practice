from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os
import random
import asyncio

app = FastAPI()

async def blink_hostname():
    while True:
        await asyncio.sleep(2)  # Blink every 2 seconds (slower)
        os.environ['HOSTNAME_BLINK'] = 'ON'
        await asyncio.sleep(1.5)  # Blink duration
        os.environ['HOSTNAME_BLINK'] = 'OFF'

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(blink_hostname())

@app.get("/", response_class=HTMLResponse)
def read_root():
    background_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))  # Random background color
    hostname_blink_style = "color: black; font-size: 24px; text-align: center;"
    hostname_blink_style += "position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);"
    hostname_blink_style += "animation: blink 1s step-end infinite;"

    html_content = f"""
    <html>
        <head>
            <style>
                body {{
                    background-color: {background_color};
                }}
                .blink {{
                    {hostname_blink_style}
                }}
                @keyframes blink {{
                    50% {{
                        opacity: 0;
                    }}
                }}
            </style>
        </head>
        <body>
            <h1 class="blink">Hello From: {os.environ.get('HOSTNAME', 'DEFAULT_ENV')}</h1>
        </body>
    </html>
    """

    return HTMLResponse(content=html_content)
