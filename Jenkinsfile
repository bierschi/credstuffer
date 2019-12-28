pipeline {
         agent any
         stages {
                 stage('Build Package') {
                     steps {
                         echo 'Build package credstuffer'
                         sh 'pip3 install -r requirements.txt'
                         //sh 'python3 setup.py bdist_wheel'
                         //sh 'sudo python3 setup.py install'
                     }
                 }
                 stage('Static Code Metrics') {

                    steps {
                        echo 'Test Coverage'

                        echo 'Style checks with pylint'
                        sh 'pylint3 --reports=y credstuffer/'
                    }

                 }
                 stage('Unit Tests') {
                    steps {
                        echo 'Test package credstuffer'
                        sh 'python3 -m unittest discover credstuffer/test/ -v'
                    }
                 }
                 stage('Build Distribution Packages') {
                    when {
                         expression {
                             currentBuild.result == null || currentBuild.result == 'SUCCESS'
                         }
                    }
                    steps {
                        echo 'Build Source Distribution'
                        sh 'python3 setup.py sdist'

                        echo 'Build Wheel Distribution'
                        sh 'python3 setup.py bdist_wheel'
                    }
                    post {
                        always {
                              archiveArtifacts (allowEmptyArchive: true,
                              artifacts: 'dist/*whl', fingerprint: true)
                        }
                    }
                 }
                 stage('Deploy To Target Server') {
                    steps {
                        echo 'Deploy credstuffer to target server'
                        sshPublisher(publishers: [sshPublisherDesc(configName: 'christian@server', transfers: [sshTransfer(cleanRemote: false, excludes: '', execCommand: 'sudo pip3 install projects/credstuffer/$BUILD_NUMBER/credstuffer-*.whl', execTimeout: 120000, flatten: false, makeEmptyDirs: false, noDefaultExcludes: false, patternSeparator: '[, ]+', remoteDirectory: 'credstuffer/$BUILD_NUMBER', remoteDirectorySDF: false, removePrefix: 'dist', sourceFiles: 'dist/*.whl')], usePromotionTimestamp: false, useWorkspaceInPromotion: false, verbose: false)])
                    }
                }

                stage('Deploy to PyPI') {
                    steps {
                        echo 'Deploy to PyPI'
                    }
                }

    }
}
