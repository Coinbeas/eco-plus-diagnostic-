# ECO Plus Diagnostic Center

Flask-based responsive website and appointment system for ECO Plus Diagnostic Center, Pabna, Bangladesh.

## Features

- Responsive healthcare homepage
- Diagnostic services and test information
- Chairman profile
- Appointment request API
- SQLite-backed persistent appointments
- Session-protected admin login and dashboard
- Admin appointment list

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

## Persistent disk configuration

By default, the app creates the database at `instance/appointments.db`. For production, point `DATABASE_PATH` to a directory on a persistent disk or mounted volume:

```env
DATABASE_PATH=/var/lib/eco-plus/appointments.db
```

The app creates the parent directory automatically when the process has permission to do so. On a Linux server, prepare the directory and grant it to the service user:

```bash
sudo mkdir -p /var/lib/eco-plus
sudo chown -R www-data:www-data /var/lib/eco-plus
sudo chmod 750 /var/lib/eco-plus
```

If the app runs as another user, replace `www-data` with that user. Back up the SQLite file regularly:

```bash
sqlite3 /var/lib/eco-plus/appointments.db ".backup '/var/backups/eco-plus-appointments.db'"
```

Do not use an ephemeral filesystem for `DATABASE_PATH`, or appointments can be lost after redeploy/restart.

## Environment variables

Copy `.env.example` to `.env` for local development. Never commit `.env` or real credentials.

- `SECRET_KEY`: required secure Flask session secret
- `ADMIN_USERNAME`: admin username
- `ADMIN_EMAIL`: optional admin email login
- `ADMIN_PASSWORD`: strong admin password
- `DATABASE_PATH`: absolute path on the persistent disk
- `COOKIE_SECURE=1`: enable when serving over HTTPS

## Admin

- Login: `/admin/login`
- Dashboard: `/admin/dashboard`
- Logout: `/admin/logout`

Change the default admin credentials before deployment.
