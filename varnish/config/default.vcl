vcl 4.0;

import directors;

backend server1 {
    .host = "gate1";
    .port = "4000";
}

backend server2 {
    .host = "gate2";
    .port = "4000";
}

backend server3 {
    .host = "gate3";
    .port = "4000";
}

sub vcl_backend_response {
    set beresp.ttl = 2s;
}

sub vcl_init {
    new vdir = directors.round_robin();
    vdir.add_backend(server1);
    vdir.add_backend(server2);
    vdir.add_backend(server3);
}

sub vcl_recv {
    # send all traffic to the director:
    set req.backend_hint = vdir.backend();
}
