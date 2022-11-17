pipeline {
	agent any
	environment {
        // CI set to true to allow it to run in "non-watch" (i.e. non-interactive) mode
        CI = 'true'
    }
	stages {
		stage('Dependency Check') {
			steps {
				git 'https://github.com/asifexplore/quiz_jenkins.git'
				dependencyCheck additionalArguments: '--format HTML --format XML', odcInstallation: 'Default'
			}
		}
		stage('Setup bridge network') {
	        agent any
				steps {
				    sh 'docker network create --driver bridge my-net'
			    }
	    }
		stage('Integration UI Test') {
			parallel {
				stage('Deploy') {
					agent any
					steps {
						sh 'chmod +x ./jenkins/scripts/deploy.sh'
						sh './jenkins/scripts/deploy.sh'
						input message: 'Finished using the web site? (Click "Proceed" to continue)'
						sh 'chmod +x ./jenkins/scripts/kill.sh'
						sh './jenkins/scripts/kill.sh'
						sh 'docker network rm my-net'
					}
				}
				stage('Headless Browser Test') {
					agent {
						docker {
							image 'maven:3-alpine'
							args '-v /root/.m2:/root/.m2 --network my-net'
						}
					}
					steps {
						sh 'mvn -B -DskipTests clean package'
						sh 'mvn test'
					}
					post {
						always {
							junit 'target/surefire-reports/*.xml'
						}
					}
				}
			}
		} // End of Integration UI Test 
		stage('Code Quality Check via SonarQube') { 
			steps { 
				script { 
					def scannerHome = tool 'SonarQube'; 
					withSonarQubeEnv('SonarQube') { 
						sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=OWASP -Dsonar.sources=. -Dsonar.host.url=http://172.20.10.2:9000 -Dsonar.login=sqp_f793cafb260b3e5366b6dee928e15e8a5829e4b6" 
					} 
				} 
			}

	}	
	post {
		success {
			dependencyCheckPublisher pattern: 'dependency-check-report.xml'
		}
		always { 
            recordIssues enabledForFailure: true, tool: sonarQube() 
        } 
	}
}