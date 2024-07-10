pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Bastian-Rojas/Docker.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                   python3 -m venv venv
                   . venv/bin/activate
                   pip install --upgrade pip
                   pip install torch torchvision torchaudio
                   pip install numpy  
                   pip install pyyaml
                   pip install ultralytics
                '''
            }
        }

        stage('Train Model') {
            steps {
                . venv/bin/activate
                sh 'python train.py --output_dir runs/train/exp --weights_path runs/train/exp/weights'
            }
        }

        stage('Validate Model') {
            steps {
                script {
                    if (fileExists('runs/train/exp/weights/best.pt')) {
                        sh 'mv runs/train/exp/weights/best.pt best.pt'
                    } else {
                        error "El archivo runs/train/exp/weights/best.pt no existe."
                    }
                }
                . venv/bin/activate
                sh 'python validate_model.py'
            }
        }

        stage('Process Image') {
            steps {
                . venv/bin/activate
                sh 'python process_image.py --model_path best.pt --image_path images/frisona.jpg'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '**/best.pt', allowEmptyArchive: true
            cleanWs()
        }

        failure {
            echo 'El pipeline ha fallado.'
        }

        success {
            echo 'El pipeline se ha completado con éxito.'
        }
    }
}