from flask import redirect, request, url_for


def query_filers():
    if request.method == 'POST':
        query = {}
        if 'available' in request.form:
            if not request.form['available'] == 'all':
                query.update({'available': request.form['available']})
        if 'domain_name' in request.form:
            if not request.form['domain_name'] == '':
                query.update({'domain': request.form['domain_name']})
        if 'domain_zone' in request.form:
            if not request.form['domain_zone'] == '':
                query.update({'suffix': request.form['domain_zone']})
        return redirect(url_for('pages.links', **query))
