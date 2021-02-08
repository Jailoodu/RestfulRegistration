<p align="center">

  <h3 align="center">RestfulRegistration</h3>

  <p align="center">
    Registration API for ConAssist.
    <br />
    <br />
    <a href="https://github.com/Jailoodu/RestfulRegistration/issues">Report Bug</a>
    ·
    <a href="https://github.com/Jailoodu/RestfulRegistration/issues">Request Feature</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

RestfulRegistration is a REST API that allows event organizers to track the status of attendees during events. It is part of the ConAssist application, which adheres to the microservices architecture. This project utilizes Google Firestore as the database which stores all of the user data.


### Built With

* [Python]()
* [Flask]()
* [Docker]()
* [Google Firestore]()


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

In order to run the project, you will need Docker installed.
* Docker
  ```sh
  Instructions: https://docs.docker.com/get-docker/
  ```

### Installation

1. Clone the repo.
   ```sh
   git clone https://github.com/Jailoodu/RestfulRegistration.git
   ```
2. Create a file in the root directory called `serviceAccount.json` by following the steps at https://cloud.google.com/iam/docs/creating-managing-service-account-keys.

3. Create a docker image for the project.
   ```sh
   docker build -t python-register:latest . 
   ```
   
4. Run the docker image that was created.
   ```sh
   docker run -d -p 5001:5001 python-register 
   ```

<!-- USAGE EXAMPLES -->
## Usage

This project is built upon RESTful architecture, therefore it is ideal if one is familiar with it. The following steps assume that you are running this application locally with the default settings. You can utilize CURL or an application like Postman to submit requests.

1. Ensure the project is running.
   ```sh
   docker ps
   ```

2. Head over to http://127.0.0.1:5001/api/, where the Swagger UI is hosted. You will be able to view API definitions and examples of all the available endpoints.

## Testing

[Pytest](https://docs.pytest.org/en/stable/) was utilized to test this repository. The unit tests can be found in `./tests/test_implementation.py`, the acceptance tests in `./tests/test_app.py`, and the stress tests in `./tests/test_stress.py`. 

To run the tests locally, the serviceAccount.json.enc file needs to be decrypted, please message the developers to request the decryption command. Then run the command `pytest --cov=api tests`. A coverage report will be generated within `./docs/coverage.html` once the tests are completed.

Travis CI is being utilized to automate testing, you can find the instance [here](https://travis-ci.org/github/Jailoodu/RestfulRegistration). 

For the Professor and TAs of 4ZP6: you've been given permission to this GitHub repository, therefore if you log into travis-ci.org, you will see the builds for this project, and be able to start a new one to run the tests. 

A static copy of the coverage report is located at `./docs/coverage.png`.

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/Jailoodu/RestfulRegistration/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/Feature`)
3. Commit your Changes (`git commit -m 'Add some Feature'`)
4. Push to the Branch (`git push origin feature/Feature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Jaison Loodu - jaison_loodu@yahoo.ca

Project Link: [https://github.com/Jailoodu/RestfulRegistration](https://github.com/Jailoodu/RestfulRegistration)





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/github_username
