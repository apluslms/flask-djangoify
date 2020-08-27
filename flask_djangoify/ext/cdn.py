def finalize(app):
    if 'USE_CDN' in app.config:
        def context_processor():
            return {'use_cdn': app.config['USE_CDN']}
        app.context_processor(context_processor)


def init_app(app):
    if 'USE_CDN' not in app.config:
        app.config['USE_CDN'] = (app.env == 'production')

    app.after_finalize.connect(finalize)
