pipeline {
    agent any

    environment {
        REMOTE_USER = 'ubuntu'
        REMOTE_HOST = '10.192.209.112'
        APACHE_URL = 'http://10.192.209.112'
    }

    stages {
        stage('SSH & Install Apache2') {
            steps {
                sshagent (credentials: ['jenkins-ssh-key']) {
                    sh """
                    ssh -t -o StrictHostKeyChecking=no $REMOTE_USER@$REMOTE_HOST '
                        echo "🔧 Updating packages..." &&
                        sudo apt update &&
                        echo "📦 Installing Apache2..." &&
                        sudo apt install -y apache2 &&
                        echo "✅ Apache installed. Restarting..." &&
                        sudo systemctl restart apache2 &&
                        echo "🚀 Apache Status:" &&
                        sudo systemctl status apache2 | head -n 10
                    '
                    """
                }
            }
        }
        stage('Verify Apache URL Reachability') {
            steps {
                sh """
                echo "🌐 Checking URL: \$APACHE_URL"
                sleep 5
                HTTP_STATUS=\$(curl -o /dev/null -s -w "%{http_code}" \$APACHE_URL)

                if [ "\$HTTP_STATUS" -eq 200 ]; then
                  echo "✅ Apache is reachable at \$APACHE_URL"
                else
                  echo "❌ Apache is NOT reachable. Status code: \$HTTP_STATUS"
                  exit 1
                fi
                """
            }
        }
    }
}
