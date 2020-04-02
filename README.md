[![Build Status](https://travis-ci.org/nyu-devops-wishlists/wishlists.svg?branch=master)](https://travis-ci.org/nyu-devops-wishlists/wishlists)
[![codecov](https://codecov.io/gh/nyu-devops-wishlists/wishlists/branch/master/graph/badge.svg)](https://codecov.io/gh/nyu-devops-wishlists/wishlists)

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

    nosetests
    
**Nose** is configured to automatically include the flags `--with-spec --spec-color` so that red-green-refactor is meaningful. If you are in a command shell that supports colors, passing tests will be green while failing tests will be red. It also has `--with-coverage` specified so that code coverage is included in the tests.

The Code Coverage tool runs with nosetests so to see how well your test cases exercise your code just run the report:

    coverage report -m

This is particularly useful because it reports the line numbers for the code that is not covered so that you can write more test cases.

When you are done, you can exit and shut down the vm with:

    exit
    vagrant halt
   
If the VM is no longer needed you can remove it with:

    vagrant destroy
