from flask import Blueprint, render_template

#create error module to register error handlers
errors = Blueprint('errors', __name__)

#register handler for 404 error
@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

#register handler for 403 error
@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

#register handler for 500 error
@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500
