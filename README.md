# Ansible Role: uberspace-web-backend

This is part of the uberspace roles collection.

This is meant to be used on your [Uberspace](https://uberspace.de/).

Please be aware, that I'm neither part of the Uberspace team, nor am I associated to them other than having some Uberspaces myself.
This project was created, because I wanted to use the roles for myself and thought they were okay-ish enough to share them.

## What is this (from the uberspace manual)

Using web backends you can connect your applications directly to our frontend to make them accessible from the outside. Traffic is proxied transparently to your application: WebSockets just work and your Host header is set correctly. If you have prior experience with RewriteRule proxies, are also much faster.

You can find the documentation of the replaced tool `uberspace web backend` in the Uberspace Manual [here](https://manual.uberspace.de/web-backends.html).

## Usage

| Variable | Choices/Default                            | Description                                                                        |
| :------: | :----------------------------------------- | :--------------------------------------------------------------------------------- |
|  route   | /                                          | The route for the backend to listen on                                             |
|   http   | false                                      | Set to {port: [your port number]} to enable a http backend                         |
|  apache  | false                                      | Use the apache server. If htto and apache is false, apache is used                 |
|  state   | <ul><li>present ✔</li><li>absent</li></ul> | "present" to enable the user, "absent" to disable it                               |
| backends | []                                         | A list of route, http, apache, state combinations to set multiple backends at once |

## Examples

### Set http backend

```yaml
- hosts: uberspace
  roles:
    - name: uberspace-web-backend
      route: isabell.example
      http:
        port: 8080
```

### Set apache backend

```yaml
- hosts: uberspace
  roles:
    - name: uberspace-web-backend
      route: isabell.example
      apache: true
```

### Delete backend

```yaml
- hosts: uberspace
  roles:
    - name: uberspace-web-backend
      route: isabell.example
      state: absent
```

### Set multiple backends

```yaml
- hosts: uberspace
  roles:
    users:
      - name: uberspace-web-backend
        route: apache.isabell.example
        apache: true
      - name: uberspace-web-backend
        route: http.isabell.example
        http: 
          port: 8080
      - name: uberspace-web-backend
        route: remove.isabell.example
        state: absent
```
