# Niranjan Kumar — Portfolio

A Flask website presenting my profile, projects, résumé, and contact form.

## Features

- Home page with professional profile and links
- Projects and résumé pages
- Contact form that stores submissions in SQLite
- Optional email notifications and protected message dashboard

## Run locally

1. Install Python 3 and the packages listed in `requirements.txt`.
2. Generate a unique secret and set it as `FLASK_SECRET_KEY` before launching the app.

   macOS/Linux:

   ```sh
   export FLASK_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
   ```

   Windows PowerShell:

   ```powershell
   $env:FLASK_SECRET_KEY = (python -c "import secrets; print(secrets.token_hex(32))")
   ```

3. Start the application:

   ```sh
   python app.py
   ```

The local server runs with debug mode disabled.

## Optional environment variables

- `ADMIN_USERNAME` and `ADMIN_PASSWORD` — enable dashboard sign-in. Both must be set; otherwise authentication fails closed.
- `EMAIL_ADDRESS` and `EMAIL_PASSWORD` — enable Gmail SMTP notifications. Without these settings, form submissions are stored locally and the site reports that email notifications are unavailable.

The SQLite database is created as `portfolio.db` when the app is started directly. Keep secret values out of source control and configure them through your hosting provider for deployment.
