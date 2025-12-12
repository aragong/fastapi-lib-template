"""Utilities used in the API."""

from __future__ import annotations

from logging import getLogger
from src.config.env import env

logger = getLogger(__name__)


def generate_root_html(
    api_name: str,
    version: str,
    favicon_path: str = "static/favicon.ico",
    logo_path: str = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRXoOGcCGYMPzSHHYK7G5YYESA_iIiFxFtMfw&s",
    description: str = "Add API description.",
    docs_path: str = f"{env.API_ROOT_PATH}/docs",
    company_name: str = "IHCantabria",
    contact_email: str = "aragong@unican.es",
) -> str:
    """Generate HTML content for the root endpoint.

    Args:
        api_name: Name of the API
        version: Version of the API
        favicon_path: Path to the favicon image
        logo_path: Path to the logo image
        description: Description of the API
        docs_path: Path to the API documentation
        company_name: Name of the company
        contact_email: Contact email address

    Returns:
        HTML content string for the root page
    """

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{api_name} - v{version}</title>
        <link rel="icon" type="image/x-icon" href="{favicon_path}">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 25%, #2c3e50 50%, #34495e 75%, #4a5568 100%);
                color: white;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
            }}
            .container {{
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 2rem;
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
                border: 1px solid rgba(255, 255, 255, 0.18);
                max-width: 800px;
                margin: 1rem;
            }}
            .logo {{
                max-width: 250px;
                height: auto;
                margin-bottom: 1rem;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            }}
            h1 {{
                font-size: 2.2rem;
                margin-bottom: 0.5rem;
                color: #ffffff;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            }}
            .version {{
                background: rgba(255, 255, 255, 0.2);
                color: white;
                padding: 0.4rem 0.8rem;
                border-radius: 25px;
                display: inline-block;
                margin-bottom: 1rem;
                font-weight: bold;
            }}
            .nav {{
                margin-bottom: 1rem;
            }}
            .nav a {{
                background: rgba(74, 144, 226, 0.3);
                color: white;
                text-decoration: none;
                padding: 0.7rem 1.5rem;
                border-radius: 25px;
                display: inline-block;
                font-weight: bold;
                border: 1px solid rgba(74, 144, 226, 0.5);
                transition: all 0.3s ease;
                font-size: 1rem;
            }}
            .nav a:hover {{
                background: rgba(74, 144, 226, 0.5);
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(74, 144, 226, 0.3);
            }}
            .description {{
                font-size: 1rem;
                line-height: 1.4;
                margin-bottom: 1rem;
                color: white;
                opacity: 0.9;
            }}
            .links {{
                display: flex;
                gap: 1rem;
                justify-content: center;
                flex-wrap: wrap;
            }}
            .link-button {{
                background: rgba(255, 255, 255, 0.2);
                color: white;
                text-decoration: none;
                padding: 0.8rem 1.5rem;
                border-radius: 10px;
                transition: all 0.3s ease;
                border: 1px solid rgba(255, 255, 255, 0.3);
                font-weight: 500;
            }}
            .link-button:hover {{
                background: rgba(255, 255, 255, 0.3);
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            }}
            .footer {{
                margin-top: 1rem;
                font-size: 0.85rem;
                opacity: 0.7;
            }}
            /* Tablet styles */
            @media (max-width: 1024px) and (min-width: 769px) {{
                .container {{
                    padding: 1.8rem;
                    margin: 1rem;
                    max-width: 90%;
                }}
                h1 {{
                    font-size: 2rem;
                }}
                .logo {{
                    max-width: 220px;
                }}
                .nav a {{
                    padding: 0.6rem 1.2rem;
                    font-size: 0.9rem;
                }}
                .description {{
                    font-size: 1rem;
                }}
            }}

            /* Mobile styles */
            @media (max-width: 768px) {{
                .container {{
                    padding: 1.5rem;
                    margin: 0.5rem;
                    max-width: 95%;
                }}
                h1 {{
                    font-size: 1.8rem;
                    margin-bottom: 0.3rem;
                }}
                .logo {{
                    max-width: 200px;
                    margin-bottom: 0.8rem;
                }}
                .description {{
                    font-size: 0.9rem;
                    line-height: 1.3;
                }}
                .nav a {{
                    padding: 0.5rem 1rem;
                    font-size: 0.85rem;
                }}
                .version {{
                    padding: 0.3rem 0.6rem;
                    font-size: 0.9rem;
                }}
                .footer {{
                    font-size: 0.8rem;
                    margin-top: 0.8rem;
                }}
                .links {{
                    gap: 0.5rem;
                }}
                .link-button {{
                    padding: 0.6rem 1rem;
                    font-size: 0.85rem;
                }}
            }}

            /* Small mobile */
            @media (max-width: 480px) {{
                body {{
                    padding: 0.5rem;
                }}
                .container {{
                    padding: 1rem;
                    margin: 0.25rem;
                    border-radius: 15px;
                    max-width: 98%;
                }}
                h1 {{
                    font-size: 1.5rem;
                    margin-bottom: 0.2rem;
                }}
                h1 img {{
                    width: 24px !important;
                    height: 24px !important;
                    margin-right: 8px !important;
                }}
                .logo {{
                    max-width: 160px;
                    margin-bottom: 0.6rem;
                }}
                .description {{
                    font-size: 0.85rem;
                    line-height: 1.25;
                    margin-bottom: 0.8rem;
                }}
                .description p {{
                    margin: 0.3rem 0;
                }}
                .nav {{
                    margin-bottom: 0.8rem;
                }}
                .nav a {{
                    padding: 0.4rem 0.8rem;
                    font-size: 0.8rem;
                    border-radius: 20px;
                }}
                .version {{
                    padding: 0.25rem 0.5rem;
                    font-size: 0.8rem;
                    margin-bottom: 0.8rem;
                }}
                .footer {{
                    font-size: 0.75rem;
                    margin-top: 0.6rem;
                    line-height: 1.2;
                }}
                .footer p {{
                    margin: 0.2rem 0;
                }}
                .links {{
                    flex-direction: column;
                    gap: 0.3rem;
                }}
                .link-button {{
                    padding: 0.5rem 0.8rem;
                    font-size: 0.8rem;
                    width: 100%;
                    text-align: center;
                }}
            }}

            /* Very small screens */
            @media (max-width: 320px) {{
                .container {{
                    padding: 0.8rem;
                    margin: 0.1rem;
                }}
                h1 {{
                    font-size: 1.3rem;
                }}
                .logo {{
                    max-width: 140px;
                }}
                .description {{
                    font-size: 0.8rem;
                }}
                .nav a {{
                    font-size: 0.75rem;
                    padding: 0.35rem 0.6rem;
                }}
                .version {{
                    font-size: 0.75rem;
                }}
                .footer {{
                    font-size: 0.7rem;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>
                <img src="{favicon_path}" alt="Icon image"
                     style="width: 32px; height: 32px; margin-right: 10px; vertical-align: middle;">
                {api_name.title()}
            </h1>
            <div class="version">Version {version}</div>
            <div class="nav">
                <a href="{docs_path}">📚 API Documentation</a>
            </div>
            <div class="description">
                <p>{description}</p>
            </div>
            <img src="{logo_path}" alt="Logo image" class="logo">
            <div class="footer">
                <p>🏢 <strong>{company_name}</strong> | Contact: {contact_email}</p>
                <p>⚙️ OpenTelemetry Enabled | 🎯 FastAPI Powered</p>
            </div>
        </div>
    </body>
    </html>
    """
