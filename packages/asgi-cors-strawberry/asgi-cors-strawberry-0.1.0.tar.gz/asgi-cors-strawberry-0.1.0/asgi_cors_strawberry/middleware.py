import fnmatch

'''
ACCESS_CONTROL_ALLOW_ORIGIN = b"Access-Control-Allow-Origin"
ACCESS_CONTROL_ALLOW_HEADERS = b"Access-Control-Allow-Headers"
ACAO_ACAH = {ACCESS_CONTROL_ALLOW_ORIGIN, ACCESS_CONTROL_ALLOW_HEADERS}

allow_all = True
hosts = []
host_wildcards = []
access_control_allow_headers = [b"content-type"]  # , b"authorization"]
'''


def cors_options(allow_all=True, hosts=[], host_wildcards=[], headers=["content-type", "authorization"]):
    hosts = set(h.encode("utf8") if isinstance(h, str) else h for h in hosts)
    host_wildcards = [
        h.encode("utf8") if isinstance(h, str) else h for h in host_wildcards
    ]
    access_control_allow_headers = [
        h.encode("utf8") if isinstance(h, str) else h for h in headers]

    return allow_all, hosts, host_wildcards, access_control_allow_headers


class CorsMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        async def _base_send(event):
            ################################################
            ACCESS_CONTROL_ALLOW_ORIGIN = b"Access-Control-Allow-Origin"
            ACCESS_CONTROL_ALLOW_HEADERS = b"Access-Control-Allow-Headers"
            ACAO_ACAH = {ACCESS_CONTROL_ALLOW_ORIGIN, ACCESS_CONTROL_ALLOW_HEADERS}
            allow_all = True
            hosts = []
            host_wildcards = []
            access_control_allow_headers = [b"content-type"]
            ################################################

            if event["type"] == "http.response.start":
                original_headers = event.get("headers") or []  # send_headers
                access_control_allow_origin = None
                if allow_all:
                    access_control_allow_origin = b"*"
                elif hosts or host_wildcards:
                    incoming_origin = dict(
                        scope.get("headers") or []).get(b"origin")
                    if incoming_origin:
                        matches_hosts = incoming_origin in hosts
                        matches_wildcards = any(
                            fnmatch.fnmatch(incoming_origin, host_wildcard)
                            for host_wildcard in host_wildcards
                        )
                        if matches_hosts or matches_wildcards:
                            access_control_allow_origin = incoming_origin

                if access_control_allow_origin:
                    # preflight in consumer -> status is 405
                    status = 200 if scope["method"] == "OPTIONS" else event["status"]
                    event = {
                        "type": "http.response.start",
                        "status": status,
                        "headers": [
                            [h for h in original_headers if h[0] not in ACAO_ACAH]
                            [ACCESS_CONTROL_ALLOW_ORIGIN,
                                access_control_allow_origin],
                            [ACCESS_CONTROL_ALLOW_HEADERS, b", ".join(
                                access_control_allow_headers)]
                        ],
                    }
            await send(event)

        # _base_send -> send in ASGIHandler or AsyncConsumer
        return await self.app(scope, receive, _base_send)
