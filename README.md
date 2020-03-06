# Wishlists

This repository contains documentation for creating a wishlist microservice as part of building an e-commerce website. All documentation is created and maintained by the wishlist squad members.

## Squad Members

Thomas Chao, Rebecca Dailey, Bea Del Rio, Isaias Martin-Hoyo & Rudmila Salek

## Setup
The best way to gain access is through Vagrant and VirtualBox. If you don't have this software already, the first step is to download and install it:

Download [VirtualBox](https://www.virtualbox.org/)

Download [Vagrant](https://www.vagrantup.com/)

Once this software is in place, perform the following command to gain access to the wishlist repository:

    git clone https://github.com/nyu-devops-wishlists/wishlists.git
    cd wishlists
    vagrant up
    vagrant ssh
    cd /vagrant

As developers, we recommend running tests before changing any code. Below is the command to run the tests using `nose`

    $ nosetests
