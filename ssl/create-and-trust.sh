generate() {
    openssl req -nodes -new -x509 -config local-host.cnf -out local-host.cert -keyout local-host.pem
}

trust() {
    sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain local-host.cert
}

generate && trust