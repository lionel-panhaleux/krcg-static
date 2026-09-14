# Web server

Serves [static.krcg.org](https://static.krcg.org) with nginx, using the `nginx_site`
role from [server-setup](https://github.com/lionel-panhaleux/server-setup): a static
site over HTTPS and plain HTTP alike, with a Let's Encrypt certificate. The host is
`strasbourg` in server-setup's `deploy-targets.yml`.

As a public site (`nginx_site_public`), every response carries CORS, directories are
listed, and plain HTTP serves the same site as HTTPS, with no redirect. `deploy.yml`
only adds the `/bust/<digits>/` cache-busting prefix. The role sets the short
`Cache-Control` lifetimes; server-setup's host setup provides gzip.

This only sets up the web server. The files still go out through the `Deployment`
and `Data` actions (or `just static` and `just data`), which rsync the build into the site
root, `/home/lpanhaleux/projects/static.krcg.org/dist`. Run it again only when the
nginx setup changes.

From this `ansible/` directory:

```bash
ansible-galaxy collection install -r requirements.yml
ansible-playbook deploy.yml --check --diff  # dry run
ansible-playbook deploy.yml
```

`inventory.yml` targets strasbourg as `deploy` with `~/.ssh/deploy`; set `DEPLOY_USER`
to connect as someone else.
