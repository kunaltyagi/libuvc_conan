# libuvc conan recipe

## Creation
```
conan new libuvc/0.1@kunaltyagi/master -t
```

## Setup and Build
```
conan source .
conan build .
conan install . libuvc/0.1@kunaltyagi/master
```

## Test and Package
```
conan test test_package libuvc/0.1@kunaltyagi/master
conan package .
conan export . libuvc/0.1@kunaltyagi/master
conan upload libuvc/0.1@kunaltyagi/master
```
