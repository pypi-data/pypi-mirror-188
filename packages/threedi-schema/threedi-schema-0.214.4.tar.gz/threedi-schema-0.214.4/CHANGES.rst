Changelog of threedi-schema
===================================================


0.214.4 (2023-01-31)
--------------------

- Properly cleanup geo-tables in migration 214.


0.214.3 (2023-01-19)
--------------------

- Adapted versioning: prefix existing versions with 0.

- Fixed deprecation warnings of Geoalchemy2 0.13.0


0.214.2 (2023-01-17)
--------------------

- Fixed packaging (also include migrations).


0.214.1 (2023-01-17)
--------------------

- Fixed packaging.


0.214.0 (2023-01-17)
--------------------

- Initial project structure created with cookiecutter and
  https://github.com/nens/cookiecutter-python-template

- Ported code from threedi-modelchecker, rearranged into
  'domain', 'application', 'infrastructure', 'migrations'.
