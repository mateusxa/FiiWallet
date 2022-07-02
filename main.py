from apscheduler.schedulers.background import BackgroundScheduler

from scripts.fii_updater import update_all
from flask_migrate import Migrate
from flask_cors import CORS

from app import app, db
CORS(app)

Migrate(app, db)

from routes.auth.fii import get, post, delete
import routes.auth.login
import routes.auth.register
import routes.fiis.register

# update_all()

sched = BackgroundScheduler(daemon=True)
sched.add_job(update_all,'interval',hours=1)
sched.start()

@app.shell_context_processor
def shell_context_processor():
    return dict(
        app=app,
        db=db,
        User=User,
        FIIs=FIIs,
        user_fiis=user_fiis,
    )

@app.route('/')
def home():
    return "Hello World!"

if __name__ == '__name__':
    app.run()
