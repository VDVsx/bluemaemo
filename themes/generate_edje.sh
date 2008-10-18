#!/bin/sh

edje_cc -v -id ../images/ -fd ../fonts/ bluemaemo.edc bluemaemo.edj 
cp bluemaemo.edj ../test

