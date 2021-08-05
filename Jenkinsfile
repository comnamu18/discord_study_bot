pipeline {
    agent any
    environment {
        DISCORD_BOT_ENV_FILE = credentials('discord-bot-env-file')
    }
    stages {
        stage('Build') {
            steps {
                echo 'Building image'
                sh '''
                docker image build --tag discord-study-bot:latest .
                '''
            }
        }
        stage('Before Deploy')
        {
            steps {
                echo 'Removing existing container'
                sh '''
                EXIST_CONTAINER=$(docker ps -a -f name=discord_study_bot | wc -l)
                if [ $EXIST_CONTAINER -gt 1 ]; then
                    docker rm -f discord_study_bot
                fi
                '''
            }
        }
        stage('Deploy')
        {
            steps {
                echo 'Creating container'
                sh '''
                docker run --detach --rm \
                --name discord_study_bot \
                --env-file $DISCORD_BOT_ENV_FILE \
                discord-study-bot:latest
                '''
            }
        }
    }
}