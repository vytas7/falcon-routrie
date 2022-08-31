import falcon
import falcon.testing
import falcon_routrie


class Resource:
    def on_get(self, req, resp):
        resp.media = {'uri_template': req.uri_template}

    def on_get_user(self, req, resp, userid):
        resp.media = {'uri_template': req.uri_template, 'userid': userid}


def test_some_routes():
    app = falcon.App(router=falcon_routrie.RoutrieRouter())
    app.add_route('/foo', Resource())
    app.add_route('/foo/bar/:userid', Resource(), suffix='user')

    client = falcon.testing.TestClient(app)

    resp1 = client.get('/users/john')
    assert resp1.status_code == 404

    resp2 = client.get('/foo/bar/e1a0c154-d881')
    assert resp2.status_code == 200
    assert resp2.json == {
        'uri_template': '/foo/bar/:userid',
        'userid': 'e1a0c154-d881',
    }
