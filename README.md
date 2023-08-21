<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->

<a name="readme-top"></a>

<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

<!-- PROJECT LOGO -->
<br />
<div align="center">

<!-- ![logo](https://user-images.githubusercontent.com/69769431/220485345-82d76424-985e-4948-871a-c847a4f745cb.png) -->

<h3 align="center">MyNintendo Scraper</h3>

  <p align="center">
    A webscraper that checks My Nintendo rewards store every hour for changes.
    <br />
    <a href="https://github.com/samau3/mynintendo-scraper"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://mynintendo-scraper.vercel.app/">View App</a>
    ·
    <a href="https://github.com/samau3/mynintendo-scraper/issues">Report Bug</a>
    ·
    <a href="https://github.com/samau3/mynintendo-scraper/issues">Request Feature</a>
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
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

<div align="center">

<!-- ![homepage](https://user-images.githubusercontent.com/69769431/220259451-28f0a532-a294-4092-bde9-bb8a3734927d.png) -->

</div>


The motivation for this project was automate the process of checking My Nintendo rewards store for new items to reduce the chance of missing out on new listings.

### Built With

- [![Typescript][typescript]][typescript-url]
- [![React][react.js]][react-url]
- [![Vercel][vercel]][vercel-url]
- [![Discord][discord]][discord-url]
- [![Express][express]][express-url]
- [![PostgreSQL][postgresql]][postgresql-url]
- [![Node][node.js]][node-url]
- [![Github Actions][github-actions]][github-actions-url]
- [![Material UI][mui]][mui-url]
- [Fly.io](https://fly.io/)
- [Axios](https://axios-http.com/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running follow these simple example steps.

### Installation

- Development Environment Setup

  - You can skip these steps below if you don't plan on submitting changes or features to the repository

- npm
  - In the `app/` directory, install the required npm packages:
  ```sh
  npm install
  ```
- pip
  - In the `server/` directory, install the required python packages:
  ```sh
  source venv/bin/activate
  pip3 install -r requirements.txt
  ```
- Discord Bot messagiing
  - This application utilizes a Discord Bot to send an automated message when changes are detected on the store front, which has private keys that cannot be shared. If one wants to replicate this in their copy of this repository, one can start [here](https://discord.com/developers/docs/resources/webhook).

4. Enter your secrets in a `.env` file

    ```env
    DATABASE_URL=YOUR_DATABASE_URL
    WEBHOOK_ID=YOUR_WEBHOOK_ID_FROM_DISCORD
    WEBHOOK_TOKEN=YOUR_WEBHOOK_TOKEN_FROM_DISCORD
    DISCORD_USER_ID=YOUR_DISCORD_USER_ID
    ```

5. Starting the application 

   ```sh
    (in the app directory) npm start
    (in the server directory with venv activated) flask run
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

### Scraping

<div align="center">

</div>

To get started with trading on **Paper Trader**, the user logins and authorizes the application to utilize their Discord profile via Discord's OAuth 2.0 implementation (Note, if the application was not previously authorized then the user will have an additional step of logging into their Discord account). Once authenticated, the user is redirected to their user profile page, displaying their account balance and investments (if any) queried from the PostgreSQL database. In addition, a JWT is generated and stored in the client's local storage such that the user's session can be maintained between visits without having to constantly reauthorize access to their Discord account if they have not logged out.


<!-- ROADMAP -->

## Roadmap

<details>
<summary> Completed Features </summary>

- [x] Start a CI/CD Pipeline
  - [x] Utilize Github Actions to deploy on main branch merge to Fly.io
- [x] Scrape My Nintendo rewards page
  - [x] Get current item listings
- [x] Display any changes to My Nintendo rewards listings
  - [x] Display what has changed
  - [x] Display timestamp of when change occurred
- [x] Display current changes if any
- [x] Utilize a useEffect to scrape as soon as web app is accessed
  - [x] Include a timestamp to show when scrape occurred at time of web app loading

</details>

<details>
<summary>Features To Implement</summary>

- [] Add tests
  - [] Test routes
  - [] Test models
- [] Improve frontend visuals

</details>

See the [open issues](https://github.com/github_username/repo_name/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the repository a star! Thanks again!

1. Fork the repository
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

Project Link: [https://github.com/samau3/mynintendo-scraper](https://github.com/samau3/mynintendo-scraper)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

- Thanks to FreeCodeCamp for the BeautifulSoup Webscraping tutorial that helped get this project started

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[product-screenshot]: images/screenshot.png
[typescript]: https://img.shields.io/badge/typescript-%23007ACC.svg?style=for-the-badge&logo=typescript&logoColor=white
[typescript-url]: https://www.typescriptlang.org/
[react.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[react-url]: https://reactjs.org/
[node.js]: https://img.shields.io/badge/node.js-6DA55F?style=for-the-badge&logo=node.js&logoColor=white
[node-url]: https://nodejs.org/en/
[discord]: https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white
[discord-url]: https://discord.com/
[postgresql]: https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white
[postgresql-url]: https://www.postgresql.org/
[firebase]: https://img.shields.io/badge/firebase-%23039BE5.svg?style=for-the-badge&logo=firebase
[firebase-url]: https://firebase.google.com/
[express]: https://img.shields.io/badge/express.js-%23404d59.svg?style=for-the-badge&logo=express&logoColor=%2361DAFB
[express-url]: https://expressjs.com/
[github-actions]: https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white
[github-actions-url]: https://docs.github.com/en/actions
[vercel]: https://img.shields.io/badge/vercel-%23000000.svg?style=for-the-badge&logo=vercel&logoColor=white
[vercel-url]: https://vercel.com/
[mui]: https://img.shields.io/badge/MUI-%230081CB.svg?style=for-the-badge&logo=mui&logoColor=white
[mui-url]: https://mui.com/