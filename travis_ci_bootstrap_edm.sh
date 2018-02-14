if [[ ${TRAVIS_OS_NAME} == "osx" ]]
then
    # download and install EDM
    wget https://package-data.enthought.com/edm/osx_x86_64/1.9/edm_1.9.1.pkg
    sudo installer -pkg edm_1.9.1.pkg -target /
else
    # download and install EDM
    wget https://package-data.enthought.com/edm/rh5_x86_64/1.9/edm_1.9.1_linux_x86_64.sh
    chmod u+x edm_1.9.1_linux_x86_64.sh
    ./edm_1.9.1_linux_x86_64.sh -b -p ~
    export PATH="~/bin:${PATH}"
fi

# install pip and invoke into default EDM environment
edm install -y pip invoke coverage
