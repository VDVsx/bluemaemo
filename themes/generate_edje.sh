#!/bin/sh

edje_cc -v -id ../images/ -fd ../fonts/ bluemaemo.edc bluemaemo.edj 
cp bluemaemo.edj ../test
edje_cc -v -id ../images/ -fd ../fonts/ elementary_theme.edc elementary_theme.edj 
cp elementary_theme.edj ../test


