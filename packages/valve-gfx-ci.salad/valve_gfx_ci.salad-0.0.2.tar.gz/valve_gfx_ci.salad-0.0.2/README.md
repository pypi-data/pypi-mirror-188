SALAD provides automatic mapping between serial consoles and their attached
test machine. This is done with a service running by default on port 8100
and a REST interface running on port 8005.

The REST API provides the following endpoints:

    curl -s http://localhost:8005/api/v1/machine/

and

    curl -s http://localhost:8005/api/v1/machine/AA:BB:CC:DD:EE:FF

Where the host "localhost", the port 8005 and the mac address AA:BB:CC:DD:EE:FF
should be replaced by valid values.
