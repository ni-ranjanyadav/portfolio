# Niranjan Kumar's Portfolio

A Flask portfolio site with project, resume, and contact pages.

## Run locally

1. Install the packages in `requirements.txt`.
2. Set a unique session secret before starting the app:

   ```sh
   # macOS/Linux
   export FLASK_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
   ```

   On Windows PowerShell, set `$env:FLASK_SECRET_KEY` to a generated random value for the current session.
3. Start the application with `python app.py`.

The local development server runs with debug mode disabled.

## Optional configuration

- `ADMIN_USERNAME` and `ADMIN_PASSWORD` configure access to the message dashboard. Without both values, login fails closed.
- `EMAIL_ADDRESS` and `EMAIL_PASSWORD` configure Gmail SMTP notifications from the contact form. Without them, messages are saved locally and the page reports that notifications are unavailable.
- The contact form stores submissions in the local `portfolio.db` SQLite database.

Never commit secret values. Use your hosting provider's secret or environment-variable settings in deployment.
