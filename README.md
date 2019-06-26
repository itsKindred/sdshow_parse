# sdshow_parse
Parses the SDDL String returned by the Windows "sc sdshow" command and outputs comprehensible service permissions.

To use the utility, simply copy-paste the permission string returned by the `sc sdshow *service*` command. The script will
then print out easy-to-understand, comprehensible strings for the User and Permissions, as well as highlight permissions
of importance.
