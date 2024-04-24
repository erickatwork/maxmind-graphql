# maxmind-graphql

GraphQL API for [MaxMind](https://github.com/maxmind/MaxMind-DB-Reader-python). Built using [starlette](https://github.com/encode/starlette) ASGI framework, and [strawberry-graphql](https://github.com/strawberry-graphql/strawberry).

## Usage

You can query a single IP:

```GraphQL
{
  enrichIp(ip: "3.3.3.3") {
    ip
    country
    city
    accuracyRadius
    continent
    continentCode
    countryCode
    latitude
    longitude
    registeredCountry
    registeredCountryCode
    timezone
    connectionType
    domain
    isp
    ispOrg
    asn
    asnOrg
  }
}
```

Or multiple IPs:

```GraphQL
{
  enrichIps(ips: ["1.1.1.1", "2.2.2.2"]) {
    ip
    country
    city
    ...
  }
}
```

And check the db metadata to check the version and dbs loaded:

```GraphQL
{
    metadata {
        binaryFormatMajorVersion
        binaryFormatMinorVersion
        nodeCount
        recordSize
        description
        buildEpoch
    }
}
```

## Development

### Local

```bash
pipenv shell
pipenv install -r requirements.txt
python app/run.py
```

Browse to `http://0.0.0.0:8000/graphql`. and run the following:

```GraphQL
{
  metadata {
    binaryFormatMajorVersion
    binaryFormatMinorVersion
    nodeCount
    recordSize
    description
    buildEpoch
  }
  enrichIp(ip: "3.3.3.3") {
    ip
    country
    city
    accuracyRadius
    continent
    continentCode
    countryCode
    latitude
    longitude
    registeredCountry
    registeredCountryCode
    timezone
    connectionType
    domain
    isp
    ispOrg
    asn
    asnOrg
  }
  enrichIps(ips: ["1.1.1.1", "2.2.2.2"]) {
    ip
    country
    city
    accuracyRadius
    continent
    continentCode
    countryCode
    latitude
    longitude
    registeredCountry
    registeredCountryCode
    timezone
    connectionType
    domain
    isp
    ispOrg
    asn
    asnOrg
  }
}
```

Or via Curl:

```bash
curl -v \
-X POST \
--location \
"http://0.0.0.0:8000/graphql" \
-H 'Content-Type: application/json' \
-d '{"query":"{\n  enrichIps(ips: [\"1.1.1.1\", \"2.2.2.2\"]) {\n    ip\n    continent\n    country\n    city\n    registeredCountry\n    timezone\n    connectionType\n    domain\n    isp\n    ispOrg\n    asn\n    asnOrg\n  }\n}"}'
```

### Docker

```bash
docker build -t maxmind .
docker run -d --rm -p 8000:80 maxmind
```

Browse to `http://127.0.0.1:8000/graphql`.
