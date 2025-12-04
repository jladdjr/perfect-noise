## Message Specification

A Perfect Noise Message consists of:
- a `blocks` file
- a `message` file

The `blocks` file contains a list of uuid strings separated by newlines.
The uuids represent the blocks needed to decrypt the message.

The `message` file is a binary file representing the encrypted content.

A message is packaged as a [tar](https://www.man7.org/linux/man-pages/man1/tar.1.html) archive that contains the above files (without any directory structure).

### Message length

The exact message length -- that is, the size of the encrypted message in bytes --
is treated like a secret.

The length of the message is given in the first block of encrypted data.

## Decrypted Message specification

Decrypting a `message` will always return a tar archive.
Packaging the message as an archive allows for metadata about the encrypted file(s)
(such as names, extensions, creation and modification timestamps, ownership, etc)
to be preserved.

The encrypted content could be a simple plaintext file,
but could also be an arbitrary file or collection of files.
