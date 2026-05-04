# Perfect Noise

!!! note

    Perfect Noise is still in development. This README describes the app's future behavior.

Perfect Noise lets you send and receive messages encrypted using a
[one-time pad](pad.md).

Most one-time pad tools are limited to encrypting a file using a flat sequence of random data.
This leaves the most onerous part -- maintaining a one-time pad -- to the user.

Perfect Noise makes maintaining a one-time effortless.
Run `pad create` to create a one-time pad that is large enough to support frequent text exchanges, images, and modestly-sized binary data.
(Want to create a larger pad? Use `--size` to specify a pad that will last longer or support exchanging bigger content).

After you create a pad, share it with the person you will be corresponding with.
It is crucial that this be done securely -- ideally through a direct, in-person exchange.

Next, run `perfect encrypt` to encrypt a file.
Behind the scenes, Perfect Noise will retrieve random blocks from your one-time pad, use them to encrypt your file, and immediately discard the blocks used for encryption so that they can never be reused (making the receiver the only one in possession of the necessary encryption key).
Metadata about which blocks were used for encryption are included alongside the encrypted file to make decryption possible.
This metadata is automatically bundled with the encrypted content, so management of this information happens behind-the-scenes without assistance from the user.

When you receive encrypted content, run `perfect decrypt` to decrypt the file.
Here again, as material from your pad is retrieved to decrypt the file, it is immediately destroyed to prevent reuse.

The only time you need to manage your `pad` is when it starts to become empty.
Run `pad info` to check the remaining pad size at any time.
When it's time to create a new pad, run `pad create` to start a fresh round of encrypted communication.

## Further reading

For a deeper explanation of one-time pads and their usage, see the overview of [core concepts](concepts.md).

For technical specifications describing how one-time pads are managed by this tool, see the [specification](specification.md).
