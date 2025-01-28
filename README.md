# 🌐 Smart Translation SaaS

**Smart Translation SaaS** is an advanced language translation platform that leverages AI to deliver humanized, context-aware translations. This solution bridges language barriers, providing seamless communication across diverse users, and includes accessibility features for users with disabilities.

---

## 🚀 Live Demo & Resources
- **Demo**: [Deployment Link](https://main.d1vie8hwpqax1c.amplifyapp.com/)
- **Video Presentation**: [Vimeo](https://vimeo.com/1004595680?share=copy)
- **Research Paper**: [ResearchPaper.pdf](https://github.com/user-attachments/files/16824493/ResearchPaper.pdf)
- **Users Traffic Chart (Regular Activity Since deployment with an Average of 300 requests a week)**: ![image](https://github.com/user-attachments/assets/48a92513-2a97-495c-883e-df1f84e207e4)
<!--
- **Project Poster**: <br /> ![Poster Screenshot](https://github.com/user-attachments/assets/ce3cff32-9343-4575-9db9-72642546cfe0)
-->
---

## 📜 Table of Contents

1. [Features](#-features)
2. [Technologies Used](#%EF%B8%8F-technologies-used)
3. [Project Structure](#-project-structure)
4. [Installation](#-installation)
5. [Running Tests](#-running-tests)
6. [Current Status](#-current-status)
7. [Contributing](#-contributing)
8. [Code of Conduct](#-code-of-conduct)
9. [Security Policy](#-security-policy)
10. [License](#-license)
11. [Contact](#-contact)

---

## 🛠️ Features

- **AI-Powered Translation**: Fine-tuned GPT-3.5 Turbo model for precise, context-aware translations between French and English.
- **Speech-to-Text**: Converts spoken language to text using Azure Cognitive Services.
- **Text-to-Speech**: Provides audible output for translated text.
- **Authentication**: Secure user login and identity management via Firebase and Okta.
- **Scalable Backend**: Built with C# and ASP.NET using the MVC design pattern.
- **Dynamic Frontend**: Developed with React.js for a responsive user interface.
- **Accessibility**: Includes features to support users with disabilities.
- **Regulatory Compliance**: Ensures high levels of security and data protection.

---

## 🖥️ Technologies Used

### **Frontend**

- [React](https://reactjs.org/): Dynamic and interactive user interface.
- [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript): Core scripting language for frontend logic.
- [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS): Styling and layout for the application.
- [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML): Markup structure for web pages.

### **Backend**

- [C#](https://learn.microsoft.com/en-us/dotnet/csharp/): Programming language for backend logic.
- [ASP.NET](https://dotnet.microsoft.com/apps/aspnet): Framework for building web apps and APIs.
- [Azure Cognitive Services](https://azure.microsoft.com/en-us/services/cognitive-services/): Speech-to-text and text-to-speech functionalities.

### **Authentication and Security**

- [Firebase](https://firebase.google.com/): User authentication and database management.
- [Okta](https://www.okta.com/): Identity and access management.

### **Build Tools & Libraries**

- [Node.js](https://nodejs.org/): JavaScript runtime environment.
- [npm](https://www.npmjs.com/): Package manager for JavaScript.
- [Webpack](https://webpack.js.org/): Module bundler.

### **Development Tools**

- [Visual Studio](https://visualstudio.microsoft.com/): Integrated development environment for backend development.
- [Visual Studio Code](https://code.visualstudio.com/): Lightweight code editor for frontend development.
- [Postman](https://www.postman.com/): API testing.
- [Git](https://git-scm.com/): Version control.

---

## 📂 Project Structure

```
AI-Translation-SaaS/
├── public/             # Static assets
├── src/                # Source code
│   ├── components/     # Reusable UI components
│   ├── pages/          # Page components
│   ├── services/       # API interaction logic
│   ├── App.jsx         # Main application component
│   └── index.jsx       # Entry point
├── backend/            # Backend API and workers
│   ├── Controllers/    # API Controllers
│   ├── Models/         # Data models
│   └── Services/       # Business logic
├── .eslintrc.cjs       # ESLint configuration
├── .gitignore          # Git ignore file
├── package.json        # Project dependencies and scripts
├── README.md           # Project documentation
└── ResearchPaper.pdf   # Research document
```

---

## 📦 Installation

To set up the project locally:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/RyanL2004/AI-Translation-SaaS.git
   ```
2. **Navigate to the project directory**:
   ```bash
   cd AI-Translation-SaaS
   ```
3. **Install dependencies**:
   ```bash
   npm install
   ```
4. **Start the frontend server**:
   ```bash
   npm start
   ```
   Access the application at `http://localhost:3000`.

5. **Run the backend server**:
   Follow the backend setup instructions in the `backend/` directory.

---

## 🧪 Running Tests

To execute tests:

```bash
npm test
```

---

## 🚧 Current Status

### In Progress

We are actively working on:

- Adding support for additional languages.
- Enhancing the user interface for better accessibility.
- Integrating advanced analytics for translation accuracy.
- Extending speech-to-text functionality to include more accents.

Stay tuned for updates!

---

## 🤝 Contributing

We welcome contributions to enhance the project! To contribute:

1. **Fork the repository**.
2. **Create a new branch**:
   ```bash
   git checkout -b feature/YourFeatureName
   ```
3. **Commit your changes**:
   ```bash
   git commit -m 'Add some feature'
   ```
4. **Push to the branch**:
   ```bash
   git push origin feature/YourFeatureName
   ```
5. **Open a Pull Request**.

Please ensure your code adheres to our coding standards and includes relevant tests.

---

## 🌟 Code of Conduct

We expect all participants to adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it to understand the standards of behavior we expect from our community.

---

## 🛡️ Security Policy

To report security vulnerabilities, please contact us directly at **securitytranslationSaaS@gmail.com**. Your report will be handled with the utmost confidentiality, and we will work to address issues promptly.

---

## 🛡️ License

This project is licensed under the [MIT License](LICENSE).

---

## 📧 Contact

For any questions or suggestions, feel free to reach out:

- **GitHub Issues**: [Create an issue](https://github.com/RyanL2004/AI-Translation-SaaS/issues)
- **Email**: rayanlouahche2004@gmail.com
- **LinkedIn**: [Rayan's Profile](https://www.linkedin.com/in/rayan-louahche/)

---

Thank you for exploring **Smart Translation SaaS**! Your feedback and contributions are highly valued.


### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
