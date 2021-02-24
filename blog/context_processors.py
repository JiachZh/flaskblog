from blog import app
from blog.models import Comments

@app.context_processor
def recent_comments():
    return dict(recent_comments=Comments.query.order_by(Comments.createdAt.desc()).limit(5).all());
