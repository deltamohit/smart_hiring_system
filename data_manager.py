# data_manager.py

# This dictionary holds predefined skills for various job roles.
# The skills should be in lowercase and ideally lemmatized/stemmed form
# to match the processed resume text.
JOB_SKILL_DATABASE = {
    "Software Engineer": [
        "python", "java", "c++", "data structure", "algorithm", "sql", "git",
        "web develop", "cloud comput", "oop", "test", "debug", "softwar develop"
    ],
    "Data Analyst": [
        "python", "r", "sql", "excel", "data visualiz", "statistic", "tableau",
        "power bi", "machine learn", "communic", "report", "analysi", "dashboard"
    ],
    "Web Developer (Frontend)": [
        "html", "css", "javascript", "react", "angular", "vue", "typescript",
        "ui/ux", "respons design", "api", "frontend", "develop", "ux design"
    ],
    "Machine Learning Engineer": [
        "python", "machine learn", "deep learn", "neural network", "data scienc",
        "statist", "algorithm", "tensor flow", "pytorch", "model develop", "evalu", "gpu"
    ],
    "DevOps Engineer": [
        "linux", "docker", "kubernetes", "aws", "azure", "ci/cd", "jenkins",
        "ansible", "terraform", "script", "cloud", "automat", "deploy"
    ],
    "UX Designer": [
        "ui/ux", "design", "figma", "sketch", "adobe xd", "prototyp", "user research",
        "wirefram", "usabil", "interact design", "visual design", "feedback"
    ]
}

# This dictionary maps missing skills to suggested courses/resources.
SKILL_COURSE_MAP = {
    "python": "Check out 'Python for Everybody' on Coursera: https://www.coursera.org/specializations/python",
    "java": "Explore 'Java Programming and Software Engineering Fundamentals' on Coursera: https://www.coursera.org/specializations/java-programming",
    "c++": "Learn C++ with 'Beginning C++ Programming - From Beginner to Beyond' on Udemy: https://www.udemy.com/course/beginning-c-plus-plus-programming/",
    "sql": "Master SQL with 'SQL for Data Science' on Coursera: https://www.coursera.org/learn/sql-for-data-science",
    "data structure": "Brush up on 'Data Structures & Algorithms' on GeeksforGeeks: https://www.geeksforgeeks.org/data-structures/",
    "algorithm": "Practice 'Algorithms, Part I' on Coursera: https://www.coursera.org/learn/algorithms-part1",
    "git": "Learn 'Git Complete: The definitive, step-by-step guide' on Udemy: https://www.udemy.com/course/git-complete/",
    "web develop": "Start with 'The Complete Web Developer in 2024' on Udemy: https://www.udemy.com/course/the-complete-web-developer-in-2024/",
    "cloud comput": "Get an introduction to 'Cloud Computing Concepts, Part 1' on Coursera: https://www.coursera.org/learn/cloud-computing",
    "oop": "Understand 'Object-Oriented Programming in Java' on Coursera: https://www.coursera.org/learn/object-oriented-programming-java",
    "machine learn": "Dive into 'Machine Learning' by Andrew Ng on Coursera: https://www.coursera.org/learn/machine-learning",
    "data visualiz": "Explore 'Data Visualization with Python' on Coursera: https://www.coursera.org/learn/python-for-data-visualization",
    "statistic": "Learn 'Statistics and R' on Coursera: https://www.coursera.org/learn/statistics-r",
    "tableau": "Become a 'Tableau 2024 Masterclass for Data Science' on Udemy: https://www.udemy.com/course/tableau10/",
    "power bi": "Master 'Microsoft Power BI Desktop for Business Intelligence' on Udemy: https://www.udemy.com/course/powerbi-desktop-for-business-intelligence/",
    "r": "Get started with 'R Programming' on Coursera: https://www.coursera.org/learn/r-programming",
    "excel": "Enhance your skills with 'Excel Skills for Business' on Coursera: https://www.coursera.org/specializations/excel",
    "html": "Learn HTML with 'HTML, CSS, and Javascript for Web Developers' on Coursera: https://www.coursera.org/learn/html-css-javascript-web-developers",
    "css": "Learn CSS with 'HTML, CSS, and Javascript for Web Developers' on Coursera: https://www.coursera.org/learn/html-css-javascript-web-developers",
    "javascript": "Learn JavaScript with 'HTML, CSS, and Javascript for Web Developers' on Coursera: https://www.coursera.org/learn/html-css-javascript-web-developers",
    "react": "Build interfaces with 'React - The Complete Guide' on Udemy: https://www.udemy.com/course/react-the-complete-guide-incl-redux/",
    "angular": "Master Angular with 'Angular - The Complete Guide' on Udemy: https://www.udemy.com/course/the-complete-guide-to-angular-2/",
    "vue": "Explore Vue.js with 'Vue JS 3 - The Complete Guide' on Udemy: https://www.udemy.com/course/vuejs-2-the-complete-guide-incl-vue-router-and-vuex/",
    "typescript": "Learn 'TypeScript: The Complete Developer's Guide' on Udemy: https://www.udemy.com/course/typescript-the-complete-developers-guide/",
    "ui/ux": "Understand 'Introduction to User Experience Design' on Coursera: https://www.coursera.org/learn/user-experience-design",
    "respons design": "Learn 'Responsive Web Design Essentials - HTML5 CSS3' on Udemy: https://www.udemy.com/course/responsive-web-design-html5-css3-beginners/",
    "api": "Understand 'APIs: The Complete Guide' on Udemy: https://www.udemy.com/course/the-complete-restful-api-with-nodejs-masterclass/",
    "deep learn": "Dive into 'Deep Learning Specialization' by Andrew Ng on Coursera: https://www.coursera.org/specializations/deep-learning",
    "neural network": "Learn 'Neural Networks and Deep Learning' on Coursera: https://www.coursera.org/learn/neural-networks-deep-learning",
    "tensor flow": "Master 'TensorFlow 2.0: Deep Learning and Artificial Intelligence' on Udemy: https://www.udemy.com/course/tensorflow-2-0-deep-learning-and-artificial-intelligence/",
    "pytorch": "Explore 'PyTorch for Deep Learning with Python' on Udemy: https://www.udemy.com/course/pytorch-for-deep-learning-with-python/",
    "linux": "Get familiar with 'Linux Command Line Basics' on Coursera: https://www.coursera.org/learn/linux-command-line",
    "docker": "Learn Docker with 'Docker & Kubernetes: The Practical Guide' on Udemy: https://www.udemy.com/course/docker-and-kubernetes-the-complete-guide/",
    "kubernetes": "Learn Kubernetes with 'Docker & Kubernetes: The Practical Guide' on Udemy: https://www.udemy.com/course/docker-and-kubernetes-the-complete-guide/",
    "aws": "Get AWS certified with 'AWS Certified Solutions Architect - Associate' on Udemy: https://www.udemy.com/course/aws-certified-solutions-architect-associate-saa-c03/",
    "azure": "Explore Azure with 'Microsoft Azure Fundamentals (AZ-900)' on Udemy: https://www.udemy.com/course/microsoft-azure-fundamentals-az-900-from-scratch-latest-2023/",
    "ci/cd": "Understand CI/CD with 'The Complete CI/CD Course' on Udemy: https://www.udemy.com/course/the-complete-cicd-course/",
    "jenkins": "Master Jenkins with 'Jenkins, From Zero To Hero' on Udemy: https://www.udemy.com/course/jenkins-from-zero-to-hero/",
    "ansible": "Automate with 'Ansible for the Absolute Beginner' on Udemy: https://www.udemy.com/course/ansible-for-the-absolute-beginner-devops/",
    "terraform": "Learn Terraform with 'HashiCorp Certified: Terraform Associate' on Udemy: https://www.udemy.com/course/terraform-associate/",
    "figma": "Design with Figma: 'Figma UI UX Design Essentials' on Udemy: https://www.udemy.com/course/figma-ui-ux-design-essentials/",
    "sketch": "Learn Sketch: 'Sketch UI UX Design' on Udemy: https://www.udemy.com/course/sketch-ui-ux-design/",
    "adobe xd": "Master Adobe XD: 'Adobe XD UI UX Design' on Udemy: https://www.udemy.com/course/adobe-xd-ui-ux-design/",
    "user research": "Understand 'User Research Methods' on Coursera: https://www.coursera.org/learn/user-research-methods",
}
