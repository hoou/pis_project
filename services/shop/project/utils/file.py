from flask import current_app


def is_uploaded_file_allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config.get('UPLOAD_ALLOWED_EXT')
