# linuxcorp-poc
"Corpnet" infrastructure with all Open Source infra in docker.

TODO: Pin all versions in /build/*/Dockerfile
TODO: Write scripts for creating users in ldap
TODO: Extend scripts for generating user custom desktop docker environment
TODO: Customize ofbiz
TODO: Customize osticket
TODO: Document all functionality & guides in dokuwiki
TODO: Set up basic monitoring per user in Prom
TODO: Set up wireguard dedicated network
TODO: Set up multiple user functionality in shared environments
TODO: Set up container environment for the above via ansible

TODO: Configure and backup ldap for basic user management
TODO: Set up Authelia in swag with ldap backing
TODO: Configure management for spawning environments per user in ldap

# Install pre-requisites
```bash
apt-get install sudo python3-pip git
python3 -m pip install ansible
```