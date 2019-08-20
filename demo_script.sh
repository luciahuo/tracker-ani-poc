#!/usr/bin/env bash

start # start the tool

help # can see all the available commands

select # get all incomplete patches

select -all # get all patches

select --dkernel ubuntu # get all ubuntu patches

select --dkernel ubuntu --verbose # get detail of ubuntu patch

# change the priority of a patch or manually modify info

select --grep "memory" -v # do research on patches that are relevant to memory

select -s "powerpc/papr_scm" # find patches in a specific area of the kernel

# see all the different query options

select -h

# edit a patch with hash d9a710e5fc4941944d565b013414e9fdc66242xx

edit d9a710e5fc4941944d565b013414e9fdc66242xx

# get patches in table form
select --subject "powerpc/pseries" --output table

# get patches for a new version of the azure-tuned kernel. developer query by date

select --after 07-01-2019 -fn linus --priority 2 -o table

select --after 07-01-2019 -fn linus --priority 2 -all -o table

# could query graphs

visualize

# send an output to email address
select -fn linus -all | send-email -to lsgsysdemo@gmail.com -subject "linus's patches"
