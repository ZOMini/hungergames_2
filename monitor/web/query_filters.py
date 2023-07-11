from flask import redirect, request, url_for


def query_filers():
    if request.method == 'POST':
        query = {}
        if 'available' in request.form:
            if not request.form['available'] == 'all':
                query.update({'available': request.form['available']})
        if 'domain' in request.form:
            if not request.form['domain'] == '':
                query.update({'domain': request.form['domain']})
        if 'suffix' in request.form:
            if not request.form['suffix'] == '':
                query.update({'suffix': request.form['suffix']})
        return redirect(url_for('pages.links', **query))
