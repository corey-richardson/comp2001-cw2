# comp2001-cw2

## Running the API via Docker

### Building the Container

```bash
(cw2) C:\PATH\comp2001-cw2\cw2>docker build -t trails-api .
(cw2) C:\PATH\comp2001-cw2\cw2>docker login
(cw2) C:\PATH\comp2001-cw2\cw2>docker tag trails-api coreyrichardson1/trails-api
(cw2) C:\PATH\comp2001-cw2\cw2>docker push coreyrichardson1/trails-api
```

### Pulling and Running the Container

```bash
(cw2) C:\PATH\comp2001-cw2\cw2>docker pull coreyrichardson1/trails-api
(cw2) C:\PATH\comp2001-cw2\cw2>docker run -p 8000:8000 coreyrichardson1/trails-api

 * Serving Flask app 'config'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8000
 * Running on http://172.17.0.2:8000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 662-058-616
```

The Flask application should be found running [here](http://127.0.0.1:8000).
