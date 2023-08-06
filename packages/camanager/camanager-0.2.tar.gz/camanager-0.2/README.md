
CAManager stands for Certificate Authority Manager. With to this tool, you can :

- list and view the metadata of all your certificates
- generate a new certificate
- sign a Certificate Signing Request
- export a certificate in PEM or PCKS#12 format (.p12
- renew a certificate
- make a backup or a restore of the CA vault


# Installation

    pip3 install camanager

# Security

- If you generate a certificate with the tool, the private key is kept in the vault
- The vault is an encrypted SQLite3 DB (using SQLCipher so AES-256)
- Passwords are requested via secure input
- No network communication

# Initial setup for the first usage

This tool doesn't generate the Certificate Authority. You must already have one or generate a new one 
([step by step guide](CREATE_CA.md)).

Once you have the Certificate Authority private and public keys, run `camanager setup`:

    $ python -m camanager setup
    Enter the password that will be used to encrypt the CA vault : [secure input, nothing will appear]
    Confirm it : [same]
    Paste your CA certificate in PEM format :
    [paste here]
    Paste your CA key in PEM format :
    [paste here]
    The vault has been successfully created.

The tool verifies that the keys match. If the private key is encrypted using a passphrase, you will be prompted for it.

The vault is saved in the "ca.vault" file of the directory you are in. You must therefore run `camanager` each time 
from the same directory if you want to use the same vault.

# Usage

You can still provide information via arguments. If information is missing, an interactive prompt will occur.

## Backup the vault

    python -m camanager backup

## Restore a backup vault

    python -m camanager restore

## List certificates

    python -m camanager [--all | --soon-expired]

- `--all` : show also the revoked/expired/renewed certificates
- `--soon-expired` : show only soon expired (less than 1 month) certificates

## Generate a new certificate

**Warning :** normally, a certificate is generated on the server and a Certificate Signing Request is generated for 
the CA.

    python -m camanager --newcert [--cn CN] [--san SAN] [--keysize <1024|2048|4096>] [--hash <sha1|sha256|sha512>]

- `--cn` : the Command Name
- `--san` : the Subject Alternative Name
- `--keysize` : the keysize : 2014, 2048 or 4096
- `--hash` : the hash algorithm : sha1, sha256 or sha512

## Sign a CSR

    python -m camanager --sign [--cn CN] [--san SAN] [csr_file]

- `--cn` : the overridden Command Name
- `--san` : the overridden  Subject Alternative Name
- `csr_file` : the Certificate Signin Request file

## Export

    python -m camanager --export --pem|--p12 [--out output_file] [certificate CN or ID]

- `--pem` or `--p12` : the output format
- `--out` : the output file
- `certificate CN or ID` : the Common Name or certificate ID that you want to export
