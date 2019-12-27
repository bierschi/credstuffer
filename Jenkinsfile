pipeline {
         agent any
         stages {
                 stage('Build') {
                     steps {
                         echo 'Build credstuffer'
                         sh 'pip3 install -r requirements.txt'
                         sh 'python3 setup.py bdist_wheel'
                         sh 'sudo python3 setup.py install'
                     }
                 }
                 stage('Test') {
                    steps {
                        echo 'Test credstuffer'
                        sh 'python3 -m unittest discover credstuffer/test/ -v'
                    }
                 }
                 stage('Deploy') {
                    steps {
                        echo "Deploy credstuffer to target server"
                        sshPublisher(publishers: [sshPublisherDesc(configName: 'christian@server', transfers: [sshTransfer(cleanRemote: false, excludes: '', execCommand: 'sudo pip3 install projects/credstuffer/$BUILD_NUMBER/credstuffer-*.whl', execTimeout: 120000, flatten: false, makeEmptyDirs: false, noDefaultExcludes: false, patternSeparator: '[, ]+', remoteDirectory: 'credstuffer/$BUILD_NUMBER', remoteDirectorySDF: false, removePrefix: 'dist', sourceFiles: 'dist/*.whl')], usePromotionTimestamp: false, useWorkspaceInPromotion: false, verbose: false)])
                    }
                }
    }
}
