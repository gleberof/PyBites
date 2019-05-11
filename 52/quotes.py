from flask import Flask, jsonify, abort, request

app = Flask(__name__)

quotes = [
    {
        "id": 1,
        "quote": "I'm gonna make him an offer he can't refuse.",
        "movie": "The Godfather",
    },
    {
        "id": 2,
        "quote": "Get to the choppa!",
        "movie": "Predator",
    },
    {
        "id": 3,
        "quote": "Nobody's gonna hurt anybody. We're gonna be like three little Fonzies here.",  # noqa E501
        "movie": "Pulp Fiction",
    },
]


def _get_quote(qid):
    for qs in quotes:
        if qid == qs['id']:
            return qs
    return None


def _quote_exists(existing_quote):
    for qs in quotes:
        if existing_quote == qs['quote']:
            return True
    return False


@app.route('/api/quotes', methods=['GET'])
def get_quotes():
    return jsonify({'quotes': quotes})


@app.route('/api/quotes/<int:qid>', methods=['GET'])
def get_quote(qid):
    resp = _get_quote(qid)
    if resp:
        return jsonify({'quotes': [resp]})
    else:
        abort(404)


@app.route('/api/quotes', methods=['POST'])
def create_quote():
    ins = request.get_json()
    if len(ins) == 0 or 'quote' not in ins or 'movie' not in ins or _quote_exists(ins['quote']):
        return '', 400
    ins['id'] = len(quotes) + 1
    quotes.append(ins)
    return jsonify({'quote': ins}), 201


@app.route('/api/quotes/<int:qid>', methods=['PUT'])
def update_quote(qid):
    upd = _get_quote(qid)
    upd_new = request.get_json()
    if upd:
        upd_id = quotes.index(upd)
        if len(upd_new) == 0:
            return '', 400
        for k,v in upd_new.items():
            quotes[upd_id][k] = v
        return jsonify({'quote': quotes[upd_id]}), 200
    else:
        return '', 404


@app.route('/api/quotes/<int:qid>', methods=['DELETE'])
def delete_quote(qid):
    qs = _get_quote(qid)
    if qs:
        quotes.remove(qs)
        return '', 204
    else:
        return '', 404
