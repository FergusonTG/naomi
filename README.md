# NAOMI

An unattended filter runner for IMAP4 mailboxes. The idea is to
allow filters to be run on an inbox, for example to move mailing
list messages to their own folder. Many GUI mail clients to this
already but I do not want to run a GUI just for the sake of
Thunderbird. The point of IMAP4 is to make mail access
independent of the device or client that the user happens to be
using at the time.

## Filters

Think of the following syntax:

If \<header> \<compares-to> \<target>,  
then \<action> the message, with optional \<destination>.

## Configuration

Naomi looks for a configuration file in the following places:

-   config.toml
-   $XDG_CONFIG_HOME/naomi/config.toml
-   $XDG_CONFIG_HOME/naomi.conf
-   $HOME/.config/naomi/config.toml
-   $HOME/.config/naomi.conf
-   $HOME/.naomi.conf

## Security

Usernames and passwords are read into memory from a dbus secret
service provider. So far, this is only KeePassXC, but others such
as Gnome Keyring can be added.

## Contact

For information, bugs, help etc, please contact me on
[FergusonTG@gmail.com](mailto:FergusonTG@gmail.com)
