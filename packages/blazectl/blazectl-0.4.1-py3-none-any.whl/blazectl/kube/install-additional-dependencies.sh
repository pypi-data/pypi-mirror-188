envsubst < blazectl/kube/karpenter_default_provisioner.yaml | kubectl apply -f -
curl -fsLO https://github.com/jetstack/cert-manager/releases/latest/download/cert-manager.yaml
kubectl apply -f cert-manager.yaml


# install mysql
# https://dev.mysql.com/doc/mysql-operator/en/mysql-operator-upgrade-from-pre-ga.html
helm repo add mysql-operator https://mysql.github.io/mysql-operator/

helm repo update

helm install my-mysql-operator mysql-operator/mysql-operator --namespace mysql-operator --create-namespace

kubectl run --rm -it myshell --image=mysql/mysql-operator -- mysqlsh root@mycluster --sql

#NAME: my-mysql-operator
#LAST DEPLOYED: Sun Nov 27 20:57:03 2022
#NAMESPACE: mysql-operator
#STATUS: deployed
#REVISION: 1
#TEST SUITE: None
#NOTES:
#Create an MySQL InnoDB Cluster by executing:
#1. When using a source distribution / git clone: `helm install [cluster-name] -n [ns-name] ~/helm/mysql-innodbcluster`
#2. When using the Helm repo from ArtifactHub
#2.1 With self signed certificates
#    export NAMESPACE="your-namespace"
#    # in case the namespace doesn't exist, please pass --create-namespace
#    helm install my-mysql-innodbcluster mysql-operator/mysql-innodbcluster -n $NAMESPACE \
#        --version 2.0.7 \
#        --set credentials.root.password=">-0URS4F3P4SS" \
#        --set tls.useSelfSigned=true
#
#2.2 When you have own CA and TLS certificates
#        export NAMESPACE="your-namespace"
#        export CLUSTER_NAME="my-mysql-innodbcluster"
#        export CA_SECRET="$CLUSTER_NAME-ca-secret"
#        export TLS_SECRET="$CLUSTER_NAME-tls-secret"
#        export ROUTER_TLS_SECRET="$CLUSTER_NAME-router-tls-secret"
#        # Path to ca.pem, server-cert.pem, server-key.pem, router-cert.pem and router-key.pem
#        export CERT_PATH="/path/to/your/ca_and_tls_certificates"
#
#        kubectl create namespace $NAMESPACE
#
#        kubectl create secret generic $CA_SECRET \
#            --namespace=$NAMESPACE --dry-run=client --save-config -o yaml \
#            --from-file=ca.pem=$CERT_PATH/ca.pem \
#        | kubectl apply -f -
#
#        kubectl create secret tls $TLS_SECRET \
#            --namespace=$NAMESPACE --dry-run=client --save-config -o yaml \
#            --cert=$CERT_PATH/server-cert.pem --key=$CERT_PATH/server-key.pem \
#        | kubectl apply -f -
#
#        kubectl create secret tls $ROUTER_TLS_SECRET \
#            --namespace=$NAMESPACE --dry-run=client --save-config -o yaml \
#            --cert=$CERT_PATH/router-cert.pem --key=$CERT_PATH/router-key.pem \
#        | kubectl apply -f -
#
#        helm install my-mysql-innodbcluster mysql-operator/mysql-innodbcluster -n $NAMESPACE \
#        --version 2.0.7 \
#        --set credentials.root.password=">-0URS4F3P4SS" \
#        --set tls.useSelfSigned=false \
#        --set tls.caSecretName=$CA_SECRET \
#        --set tls.serverCertAndPKsecretName=$TLS_SECRET \
#        --set tls.routerCertAndPKsecretName=$ROUTER_TLS_SECRET

