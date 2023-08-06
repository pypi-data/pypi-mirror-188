![Build Status](https://drone.mcos.nc/api/badges/scrippy/scrippy-remote/status.svg) ![License](https://img.shields.io/static/v1?label=license&color=orange&message=MIT) ![Language](https://img.shields.io/static/v1?label=language&color=informational&message=Python)

![Scrippy, mon ami le scrangourou](./scrippy-remote.png "Scrippy, mon ami le scrangourou")

# `scrippy_remote`

Client _SSH/SFTP/FTP_ pour le cadriciel [`Scrippy`](https://codeberg.org/scrippy).

## Prérequis

### Modules Python

#### Liste des modules nécessaires

Les modules listés ci-dessous seront automatiquement installés.

- paramiko

## Installation

### Manuelle

```bash
git clone https://codeberg.org/scrippy/scrippy-remote.git
cd scrippy-remote
sudo python3 -m pip install -r requirements.txt
make install
```

### Avec `pip`

```bash
pip3 install scrippy-remote
```

### Utilisation

### `scrippy_remote`

Ce module offre l'ensemble des objets, méthodes et fonctions permettant les opérations sur les hôtes distants accessibles via _SSH/SFTP_ ou _FTP_:
- Exécution de commandes sur hôte distant
- Copie de répertoires/fichiers sur hôte distant
- Suppression de répertoires/fichiers sur hôte distant
- Copie de fichiers entre hôtes distants (la machine locale agissant comme tampon)
- ...

**Attention:** Il appartient au développeur du script de penser à fermer la connexion après usage.

Le module `scrippy_remote.remote` fournit plusieurs objets pour transférer des fichiers via _SFTP_, _FTP(es)_ ou _CIFS_ pour transférer des fichiers et _SSH_ pour l'exécution distante de commandes.

Le code source du module `scrippy_remote.remote` et de ses sous-modules est également largement commenté et reste la meilleure source de documentation.

#### SSH/SFTP
##### Exécuter une commande sur un hôte distant:

```python
import logging
from scrippy_remote import remote

remote_host = "srv.flying.circus"
remote_port = 22
remote_user = "luigi.vercotti"
key_filename = "/home/luigi.vercotti/.ssh/id_rsa"
password = "dead_parrot"

with remote.Ssh(username=remote_user,
                hostname=remote_host,
                port=remote_port,
                key_filename=key_filename,
                password=password) as host:
  stdout = host.exec_command("ls /home/luigi.vercotti", return_stdout=True)
  if stdout["exit_code"] == 0:
    for line in stdout["stdout"]:
      logging.info(line)
```

##### Récupérer un fichier distant:

```python
import logging
from scrippy_remote.remote import Ssh
from scrippy_remote import ScrippyRemoteError

remote_host = "srv.flying.circus"
remote_port = 22
remote_user = "luigi.vercotti"
remote_path = "/home/luigi.vercotti/piranha_brothers_files"
key_filename = "/home/luigi.vercotti/.ssh/id_rsa"
password = "dead_parrot"
local_path = "/home/harry.fink"
pattern = ".*"
recursive = True
delete = False
exit_on_error = True

with remote.Ssh(username=remote_user,
                hostname=remote_host,
                port=remote_port,
                key_filename=key_filename,
                password=password) as host:
  try:
    err = host.sftp_get(remote_path=remote_path,
                        local_path=local_path,
                        pattern=pattern,
                        recursive=recursive,
                        delete=delete,
                        exit_on_error=exit_on_error)
    logging.info("Errors: {}".format(err))
  except ScrippyRemoteError as e:
    logging.critical("{}".format(e))
```

##### Transférer des fichiers vers un hôte distant:

```python
from scrippy_remote.remote import Ssh
from scrippy_remote import ScrippyRemoteError

remote_host = "srv.flying.circus"
remote_port = 22
remote_user = "luigi.vercotti"
remote_path = "/home/luigi.vercotti"
key_filename = "/home/luigi.vercotti/.ssh/id_rsa"
password = "dead_parrot"
local_path = "/home/harry.fink"
pattern = ".*"
recursive = True
delete = True
exit_on_error = True

with Ssh(username=remote_user,
         hostname=remote_host,
         port=remote_port,
         key_filename=key_filename) as host:
  try:
    err = host.sftp_put(local_path=local_path,
                        remote_path=remote_path,
                        pattern=pattern,
                        recursive=recursive,
                        delete=delete,
                        exit_on_error=exit_on_error)
    logging.info("Errors: {}".format(err))
  except ScrippyRemoteError as e:
    logging.critical("{}".format(e))
```

#### FTP

##### Envoi de fichier

```python
remote_host = "srv.flying.circus"
remote_port = 21
remote_user = "luiggi.vercotti"
local_file = "/home/luiggi.vercotti/parrot.txt"
remote_dir = "dead/parrot"
password = "d34dp4rr0t"
ftp_tls = True
ftp_explicit_tls = True
ftp_ssl_verify = False
# Si `ftp_create_dir` vaut `True`, l'arborescence locale sera recrée sur l'hôte distant
ftp_create_dir = True

# Copie le fichier local "/home/luiggi.vercotti/parrot.txt" dans
# le répertoire distant "dead/parrot/home/luiggi.vercotti"
with Ftp(username=remote_user,
          hostname=remote_host,
          port=remote_port,
          password=password,
          tls=ftp_tls,
          explicit=ftp_explicit_tls,
          ssl_verify=ftp_ssl_verify) as host:
  host.put_file(local_file=local_file,
                remote_dir=remote_dir,
                create_dir=ftp_create_dir)
```

##### Lister les fichiers d'un répetoire distant

```python
remote_host = "srv.flying.circus"
remote_port = 21
remote_user = "luiggi.vercotti"
remote_dir = "dead/parrot"
password = "d34dp4rr0t"
# Pattern est une expression régulière
pattern = ".*\.txt"
ftp_tls = True
ftp_explicit_tls = True
ftp_ssl_verify = False

# Liste tous les fichiers *.txt du répertoire distant "dead/parrot"
with Ftp(username=remote_user,
           hostname=remote_host,
           port=remote_port,
           password=password,
           tls=ftp_tls,
           explicit=ftp_explicit_tls,
           ssl_verify=ftp_ssl_verify) as host:
    files = host.list(remote_dir=remote_dir,
                      pattern=pattern)
```


##### Récupère un fichier distant

```python
remote_host = "srv.flying.circus"
remote_port = 21
remote_user = "luiggi.vercotti"
remote_dir = "dead/parrot"
password = "d34dp4rr0t"
remote_file = "parrot.txt"
local_dir = "/home/luiggi.vercotti"
# Si `ftp_create_dir` vaut `True`, l'arborescence distante sera recrée sur l'hôte local
ftp_create_dir = True
ftp_tls = True
ftp_explicit_tls = True
ftp_ssl_verify = False

with Ftp(username=remote_user,
          hostname=remote_host,
          port=remote_port,
          password=password,
          tls=ftp_tls,
          explicit=ftp_explicit_tls,
          ssl_verify=ftp_ssl_verify) as host:
  remote_file = os.path.join(remote_dir, remote_file)
  host.get_file(remote_file=remote_file,
                local_dir=local_dir,
                create_dir=ftp_create_dir)
```

##### Supression d'un fichier distant

```python
remote_host = "srv.flying.circus"
remote_port = 21
remote_user = "luiggi.vercotti"
remote_dir = "dead/parrot"
password = "d34dp4rr0t"
remote_file = "parrot.txt"
ftp_tls = True
ftp_explicit_tls = True
ftp_ssl_verify = False

with Ftp(username=remote_user,
          hostname=remote_host,
          port=remote_port,
          password=password,
          tls=ftp_tls,
          explicit=ftp_explicit_tls,
          ssl_verify=ftp_ssl_verify) as host:
  remote_file = os.path.join(remote_dir, remote_file)
  host.delete_remote_file(remote_file)
```

##### Suppression d'un répertoire distant

Le répertoire sera supprimé unqiuement s'il est vide.

```python
remote_host = "srv.flying.circus"
remote_port = 21
remote_user = "luiggi.vercotti"
remote_dir = "dead/parrot"
password = "d34dp4rr0t"
ftp_tls = True
ftp_explicit_tls = True
ftp_ssl_verify = False

with Ftp(username=remote_user,
           hostname=remote_host,
           port=remote_port,
           password=password,
           tls=ftp_tls,
           explicit=ftp_explicit_tls,
           ssl_verify=ftp_ssl_verify) as host:
  host.delete_remote_dir(remote_dir)
```

---

#### CIFS

Exemple d'utilisation :

```python
with Cifs(
  hostname='SRV2GNC.gnc.recif.nc',
  shared_folder='BackupConfluence',
  username='svc.conf-bkp',
  password='MonSuperMotDePasse') as cifs:

  cifs.create_directory('myfolder')

  cifs.put_file(local_filepath='./mlocal-file.txt', remote_filepath='myfolder/remote-file.txt')

  cifs.get_file(remote_filepath='myfolder/remote-file.txt', local_filepath='./copy.txt')

  with cifs.open_for_write('myfolder/new-remote-file.txt') as file:
    file.write(b'Hello from cifs.open_for_write')

  with cifs.open_for_read('myfolder/new-remote-file.txt') as file:
    print(file.readlines())

  cifs.delete_directory_content('myfolder')
```

---
