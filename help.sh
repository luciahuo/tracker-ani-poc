#!/usr/bin/env bash
printf "====================== ABOUT ======================
The tracker maintains a database of all Linux kernel patches owned by Microsoft developers
and keeps track of their states in the patch pipeline.
These are the patch states :
      'ACCEPTED - linux-next',
      'PENDING - distro',
      'ACCEPTED - distro',
      'TESTING - microsoft',
      'SIGNED-OFF - microsoft',
      'AVAILABLE TO CUSTOMER',
      'AVAILABLE IN AZURE'\n";
echo "====================== To start querying the patch database ====================== ";
python3 selectp.py --help;
printf "\n";
echo "====================== To send output to a recipient ====================== ";
python3 send-email.py --help;
printf "\n";
echo "====================== To edit a patch in the database ====================== ";
python3 edit.py --help;
printf "\n";
echo "====================== To visualize patches in the database ====================== ";
printf "run using command \' visualize \'"
printf "\n";
