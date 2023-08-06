# sysnet-directory

Tento balíček obsahuje procedury pro prohledávání osob a skupin na serveru LDAP (AD) 
a extrakci údajů organizační struktury ze získaných hodnot.
Je určen primárně pro projekt eSMLOUVY MŽP.

## Požadavky

Python 3.9+

## Instalace a použití
### pip install sysnet-shopping

(pokud potřebujete ke spuštění  `pip` with oprávnění rool: `sudo pip install sysnet-directory`)

Pak importujte balíček:

```python
import directory
```

### Setuptools

Instalace via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user sysnet-directory
```
(nebo `sudo python setup.py install sysnet-directory` pro instalaci balíčku pro všechny uživatele)

A import balíčku:

```python
import directory
```

## Použití v programu

Balíček poskytuje singleton `DIRECTORY_FACTORY`, který obsahuje veškerou funkcionalitu. 

### Vyhledání osoby

KLíčovým slovem pro hledání osoby může být jméno, adresa elektronické pošty nebo název funkce 
(to vše včetně zástupných znaků). Vrací seznam (list) slovníků (dictinary).

    from directory.factory import DirectoryFactory
    ...
    factory = DirectoryFactory()
    user_list = factory.get_user('Jos*')
    user_list = factory.get_all_users()

Pro případ potřeby lze tuto funkci zavolat jako "raw". Pak vrací surovou odpověď LDAP serveru. 
    
    user_list = factory.get_user_raw('Jos*')
    
### Vyhledání skupiny

KLíčovým slovem pro hledání skupiny je její název včetně zástupných znaků. Vrací seznam (list) slovníků (dictinary).

    ...
    group_list = factory.get_group('*3')
    group_list = factory.get_all_groups()

Pro případ potřeby lze tuto funkci zavolat jako "raw". Pak vrací surovou odpověď LDAP serveru. 
    
    user_list = factory.get_group_raw('Jos*')

### Organizační struktura

Factory obsahuje funkcionalitu, která dokáže z LDAP dat extrahovat organizační strukturu. 
Organizační struktura je ve stromové formě. Uzly jsou propojeny oběma směry. 

    ...
    os = factory.get_org_structure()

## Systémové proměnné

Nastavení factory je řízeno systémovými proměnnými

- **LDAP_SERVER_URI** - ve formátu např `ldap://localhost:389`
- **LDAP_BIND_DN** - přihlašovací jméno k serveru
- **LDAP_BIND_PASSWORD** - heslo k přihlašovacímu jménu
- **LDAP_BASE_DN** - základní kontext. Např. `OU=eSML,DC=ad,DC=mzp,DC=cz`

Implicitní nastavení nebo nastavení přes systémové proměnné lze vždy přebít ruční operací **reset**

    factory = DirectoryFactory(uri=<uri>, bind_dn=<name>, bind_password=<password>, base_dn=<context>)
    ...
    nebo
    ...
    factory.reset(uri=<uri>, bind_dn=<name>, bind_password=<password>, base_dn=<context>)
