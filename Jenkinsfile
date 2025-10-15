stage('Build and Test') {
    steps {
        dir('backend') {
            echo "🔧 Setting up Python Virtual Environment..."
            sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
            '''
        }
    }
}
