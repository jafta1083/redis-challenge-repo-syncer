This repo syncs solution starter repositories for the [Build Your Own
Redis](https://rohitpaulk.com/articles/redis-challenge) challenge.

While each language has different build tooling, there are some things common
between all of them:

- A detailed README
- Makefile & commands to run tests

This repo handles creating solution starter repositories and keeping them in
sync.

### Usage

- make `sync` will create pull requests on each starter repository (if needed)
- Once you've vetted the PRs, use
  [`hubmerge`](https://github.com/rohitpaulk/hubmerge) to merge them
