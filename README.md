# black-clover

<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->
<!--
*** Markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
-->


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="app/assets/static/images/logo.png" alt="Logo" width="80" 
height="80">
  </a>

<h3 align="center">black-clover</h3>

  <p align="center">
    Black Clover RESTful API project based on FastAPI.
    <br />
    <a href="https://github.com/jpcadena/black-clover"><strong>Explore the docs »</strong></a>
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
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
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->

## About the project

This project is about Black Clover.

![Project][project-screenshot]

In the Clover Kingdom, The Wizard King requires designing a system for the magic academy; this must perform the registration of the student's request and the random assignment of the Grimoire to him. The level of these Grimoires is categorized by the type of clover on the cover:
* Sincerity – 1-leaf clover.
* Hope – 2-leaf clover.
* Love – 3-leaf clover.
* Good Fortune - 4-leaf clover.
* Despair – 5-leaf clover.

Students will have one of the following magic affinities:
* Darkness
* Light
* Fire
* Water
* Wind
* Earth

For this requirement it is required to expose a Rest API, built with the aforementioned tools.
The endpoints necessary to support the following operations must be exposed:
* Send application for admission.
* Update admission application.
* Update application status.
* Consult all requests.
* Consult Grimoire assignments.
* Delete application for admission.

Once the application is approved, the self-assignment of the Grimoire and the cover must be made.
Applications for admission must indicate at least the following information of the applicant:
* Name (only letters, maximum 20 characters).
* Last name (letters only, maximum 20 characters).
* Identification (numbers and letters, maximum 10 characters).
* Age (only numbers, 2 digits).
* Magical Affinity (mentioned above).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built with

* [![Python][Python]][python-url]
* [![FastAPI][FastAPI]][fastapi-url]
* [![Pydantic][Pydantic]][pydantic-url]
* [![Starlette][starlette]][starlette-url]
* [![Uvicorn][uvicorn]][uvicorn-url]
* [![Gunicorn][gunicorn]][gunicorn-url]
* [![PostgreSQL][postgresql]][postgresql-url]
* [![jwt][jwt]][jwt-url]
* [![MJML][mjml]][mjml-url]
* [![HTML5][html5]][html5-url]
* [![Pytest][pytest]][pytest-url]
* [![Pylint][pylint]][pylint-url]
* [![Pycharm][Pycharm]][Pycharm-url]
* [![Markdown][Markdown]][Markdown-url]
* [![Swagger][Swagger]][Swagger-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->

## Getting started

### Prerequisites

* [Python 3.10+][Python-docs]

### Installation

1. Clone the **repository**
    ```
    git clone https://github.com/jpcadena/black-clover.git
    ```
2. Change the directory to **root project**
    ```
    cd black-clover
    ```
3. Create a **virtual environment** *venv*
    ```
    python3 -m venv venv
    ```
4. Activate **environment** in Windows
    ```
    .\venv\Scripts\activate
    ```
5. Or with Unix/Mac OS X
    ```
    source venv/bin/activate
    ```
6. Install requirements with PIP
    ```
    pip install -r requirements.txt
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->

### Usage

1. If found **sample.env**, rename it to **.env**.
2. Replace your **credentials** into the *.env* file.
3. Execute with console
    ```
    python main.py
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->

## Contributing

[![GitHub][GitHub]][github-url]

If you have a suggestion that would make this better, please fork the repo and
create a pull request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Use docstrings with **reStructuredText** format by adding triple double quotes
**"""** after function definition.\
Add a brief function description, also for the parameters including the return
value and its corresponding data type.\
Please use **linting** to check your code quality
following [PEP 8](https://peps.python.org/pep-0008/).\
Check documentation
for [Visual Studio Code](https://code.visualstudio.com/docs/python/linting#_run-linting)
or [Jetbrains Pycharm](https://github.com/leinardi/pylint-pycharm/blob/master/README.md).\
Recommended plugin for
autocompletion: [Tabnine](https://www.tabnine.com/install)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->

## License

Distributed under the MIT License.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->

## Contact

- [![LinkedIn][LinkedIn]][linkedin-url]
- [![Outlook][Outlook]](mailto:jpcadena@espol.edu.ec?subject=[GitHub]black-clover)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[LinkedIn]: https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white

[linkedin-url]: https://linkedin.com/in/juanpablocadenaaguilar

[Outlook]: https://img.shields.io/badge/Microsoft_Outlook-0078D4?style=for-the-badge&logo=microsoft-outlook&logoColor=white

[project-screenshot]: app/assets/static/images/project.png

[Python-docs]: https://docs.python.org/3.10/

[Python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54

[FastAPI]: https://img.shields.io/badge/FastAPI-FFFFFF?style=for-the-badge&logo=fastapi

[Pydantic]: https://img.shields.io/badge/Pydantic-FF43A1?style=for-the-badge&logo=pydantic&logoColor=white

[Starlette]: https://img.shields.io/badge/Starlette-392939?style=for-the-badge&logo=starlette&logoColor=white

[Uvicorn]: https://img.shields.io/badge/Uvicorn-2A308B?style=for-the-badge&logo=uvicorn&logoColor=white

[Gunicorn]: https://img.shields.io/badge/Gunicorn-489846?style=for-the-badge&logo=gunicorn&logoColor=white

[Pylint]: https://img.shields.io/badge/linting-pylint-yellowgreen

[Pytest]: https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white

[PostgreSQL]: https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white

[html5]: https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white

[MJML]: https://img.shields.io/badge/MJML-EB5F3F?style=for-the-badge&logo=mjml&logoColor=white

[JWT]: https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens

[PyCharm]: https://img.shields.io/badge/PyCharm-21D789?style=for-the-badge&logo=pycharm&logoColor=white

[Markdown]: https://img.shields.io/badge/Markdown-000000?style=for-the-badge&logo=markdown&logoColor=white

[Swagger]: https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white

[python-url]: https://www.python.org/

[fastapi-url]: https://fastapi.tiangolo.com

[pydantic-url]: https://docs.pydantic.dev

[starlette-url]: https://www.starlette.io/

[uvicorn-url]: https://www.uvicorn.org/

[gunicorn-url]: https://gunicorn.org/

[pylint-url]: https://www.pylint.org/

[pytest-url]: https://docs.pytest.org/en/7.2.x/

[postgresql-url]: https://www.postgresql.org/

[html5-url]: https://developer.mozilla.org/en-US/docs/Glossary/HTML5

[mjml-url]: https://mjml.io/

[jwt-url]: https://jwt.io/

[Pycharm-url]: https://www.jetbrains.com/pycharm/

[Markdown-url]: https://daringfireball.net/projects/markdown/

[Swagger-url]: https://swagger.io/

[GitHub]: https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white

[GitHub-url]: https://github.com/jpcadena/black-clover
