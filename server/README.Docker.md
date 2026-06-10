### Docker usage

Docker is used for **production deployment** on Fly.io, not for day-to-day local development. For local development, use `uv sync` and `uv run flask run` (see the root [README.md](../README.md)).

### Building the production image

From the `server/` directory:

```sh
docker build -f dockerfile -t mynintendo-scraper .
```

On Apple Silicon, build for the Fly.io platform:

```sh
docker build --platform=linux/amd64 -f dockerfile -t mynintendo-scraper .
```

### Deploying to Fly.io

Deployments are handled automatically via GitHub Actions on merge to `main`. To deploy manually:

```sh
flyctl deploy --remote-only
```

### References

* [uv Docker integration](https://docs.astral.sh/uv/guides/integration/docker/)
* [Docker's Python guide](https://docs.docker.com/language/python/)
