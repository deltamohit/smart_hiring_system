# company_database.py

# Company → Job Roles → Required Skills mapping
# Skills are in preprocessed form (lowercase, stemmed)
COMPANY_JOB_SKILLS = {
    "Allianz Services": {
        "Associate-Customer Service": ["commun", "custom", "servic", "problem", "solv", "english", "crm", "support"]
    },
    "Amazon": {
        "Support Engineer III": ["linux", "troubleshoot", "network", "aws", "cloud", "support", "python", "sql"]
    },
    "Cognizant": {
        "Programmer Analyst Trainee": ["python", "java", "sql", "programm", "algorithm", "data", "structur", "oop"]
    },
    "Infosys": {
        "Specialist Programmer": ["java", "python", "spring", "microservic", "rest", "api", "sql"],
        "Systems Engineer Trainee": ["programm", "java", "python", "sql", "algorithm"],
        "Digital Specialist Engg": ["cloud", "devops", "docker", "kubernet", "python", "aws"]
    },
    "IBM": {
        "Software Developer": ["python", "java", "javascript", "sql", "cloud", "api", "develop"]
    },
    "UST": {
        "Developer I - Software Engineering.": ["python", "java", "javascript", "sql", "git", "web", "develop"],
        "Data Scientist": ["python", "machin", "learn", "statist", "sql", "data", "scienc", "model"]
    },
    "Equifax": {
        "Software Engineer": ["java", "python", "sql", "softwar", "develop", "api", "cloud"]
    },
    "Experion": {
        "Associate Software Engineer": ["python", "java", "javascript", "sql", "web", "develop", "git"]
    },
    "EY Gds": {
        "Associate Software Engineer": ["python", "java", "sql", "cloud", "develop", "algorithm"]
    },
    "Envestnet": {
        "Developer": ["java", "python", "sql", "develop", "api", "web"],
        "Engineer – QA": ["test", "qa", "selenium", "automat", "java", "python"],
        "Cloud Platform Engineer": ["cloud", "aws", "azure", "docker", "kubernet", "devops"]
    },
    "InApp": {
        "Associate Software Engineer": ["python", "java", "javascript", "react", "sql", "develop"]
    },
    "H&R Block": {
        "Associate Software Engineer": ["java", "python", "sql", "develop", "web", "api"]
    },
    "Mitsogo": {
        "Software Engineer": ["python", "java", "sql", "develop", "api"],
        "Product Evangelist": ["commun", "market", "product", "present", "technic"]
    },
    "NeoITO": {
        "Associate Software Engg": ["python", "javascript", "react", "sql", "web", "develop"],
        "Associate Ui/UX Designer": ["uiux", "figma", "design", "prototyp", "sketch"],
        "Associate Business Analyst": ["sql", "data", "analysi", "requir", "commun", "excel"]
    },
    "NexoMira": {
        "Software Engineer": ["python", "java", "javascript", "sql", "develop"]
    },
    "Simplogics": {
        "Software Engineer Trainee": ["python", "java", "sql", "develop", "programm"]
    },
    "ThinkPalm": {
        "Software Engineer Trainee": ["python", "java", "c", "embedd", "develop"]
    },
    "Cavli Wireless": {
        "Junior System Engineer": ["embedd", "c", "linux", "iot", "electr"]
    },
    "Quest Global": {
        "Trainee Engineer": ["mechan", "design", "cad", "solidwork", "autocad"]
    },
    "CommandTech": {
        "Mechanical BIM Engineer": ["bim", "revit", "mechan", "design", "autocad"]
    },
    "Reflections Info Systems": {
        "Junior Data Engineer": ["python", "sql", "data", "etl", "spark", "hadoop"]
    },
    "Federal Bank": {
        "Customer Service Associate": ["commun", "custom", "servic", "financ", "bank", "english"]
    },
    "G10X": {
        "Internal Trainee": ["python", "java", "programm", "develop", "learn"]
    },
}

# Course recommendations
# Course recommendations with FULL URLs
SKILL_COURSE_MAP = {
    "python": "Python for Everybody - Coursera: https://www.coursera.org/specializations/python",
    "java": "Java Programming - Coursera: https://www.coursera.org/specializations/java-programming",
    "sql": "SQL for Data Science - Coursera: https://www.coursera.org/learn/sql-for-data-science",
    "javascript": "JavaScript Complete Guide - Udemy: https://www.udemy.com/course/javascript-the-complete-guide-2020-beginner-advanced/",
    "react": "React Complete Guide - Udemy: https://www.udemy.com/course/react-the-complete-guide-incl-redux/",
    "machin": "Machine Learning by Andrew Ng - Coursera: https://www.coursera.org/learn/machine-learning",
    "learn": "Machine Learning by Andrew Ng - Coursera: https://www.coursera.org/learn/machine-learning",
    "cloud": "Cloud Computing Basics - Coursera: https://www.coursera.org/learn/cloud-computing",
    "aws": "AWS Certified Solutions Architect - Udemy: https://www.udemy.com/course/aws-certified-solutions-architect-associate-saa-c03/",
    "docker": "Docker & Kubernetes - Udemy: https://www.udemy.com/course/docker-and-kubernetes-the-complete-guide/",
    "kubernet": "Docker & Kubernetes - Udemy: https://www.udemy.com/course/docker-and-kubernetes-the-complete-guide/",
    "linux": "Linux Administration - Udemy: https://www.udemy.com/course/linux-administration-bootcamp/",
    "embedd": "Embedded Systems - Coursera: https://www.coursera.org/specializations/embedded-systems",
    "uiux": "UI/UX Design Specialization - Coursera: https://www.coursera.org/specializations/ui-ux-design",
    "figma": "Figma UI UX Design - Udemy: https://www.udemy.com/course/figma-ui-ux-design-essentials/",
    "design": "UI/UX Design Specialization - Coursera: https://www.coursera.org/specializations/ui-ux-design",
    "data": "Data Science Specialization - Coursera: https://www.coursera.org/specializations/jhu-data-science",
    "commun": "Business Communication - Coursera: https://www.coursera.org/learn/wharton-communication-skills",
    "algorithm": "Algorithms Part I - Coursera: https://www.coursera.org/learn/algorithms-part1",
    "structur": "Data Structures & Algorithms - GeeksforGeeks: https://www.geeksforgeeks.org/data-structures/",
    "oop": "Object-Oriented Programming in Java - Coursera: https://www.coursera.org/learn/object-oriented-java",
    "programm": "Python Programming - Coursera: https://www.coursera.org/learn/python",
    "develop": "Full Stack Web Developer - Udemy: https://www.udemy.com/course/the-complete-web-developer-zero-to-mastery/",
    "web": "Web Development Bootcamp - Udemy: https://www.udemy.com/course/the-complete-web-development-bootcamp/",
    "api": "REST API Design - Udemy: https://www.udemy.com/course/rest-api-flask-and-python/",
    "rest": "REST API Design - Udemy: https://www.udemy.com/course/rest-api-flask-and-python/",
    "spring": "Spring Framework - Udemy: https://www.udemy.com/course/spring-hibernate-tutorial/",
    "microservic": "Microservices with Spring - Udemy: https://www.udemy.com/course/microservices-with-spring-boot-and-spring-cloud/",
    "devops": "DevOps Beginners to Advanced - Udemy: https://www.udemy.com/course/decodingdevops/",
    "git": "Git Complete Guide - Udemy: https://www.udemy.com/course/git-complete/",
    "test": "Software Testing - Udemy: https://www.udemy.com/course/testerbootcamp/",
    "qa": "QA Manual Testing - Udemy: https://www.udemy.com/course/qa-software-testing-training-course/",
    "selenium": "Selenium WebDriver with Java - Udemy: https://www.udemy.com/course/selenium-real-time-examplesinterview-questions/",
    "automat": "Test Automation - Udemy: https://www.udemy.com/course/test-automation-framework-using-selenium/",
    "azure": "Microsoft Azure Fundamentals - Udemy: https://www.udemy.com/course/microsoft-azure-beginners-guide/",
    "troubleshoot": "Troubleshooting Skills - Pluralsight: https://www.pluralsight.com/courses/troubleshooting-skills",
    "network": "Computer Networking - Coursera: https://www.coursera.org/learn/computer-networking",
    "support": "IT Support Fundamentals - Coursera: https://www.coursera.org/learn/technical-support-fundamentals",
    "custom": "Customer Service Skills - Coursera: https://www.coursera.org/learn/customer-service",
    "servic": "Customer Service Skills - Coursera: https://www.coursera.org/learn/customer-service",
    "problem": "Problem Solving - Coursera: https://www.coursera.org/learn/problem-solving",
    "solv": "Problem Solving - Coursera: https://www.coursera.org/learn/problem-solving",
    "english": "Business English - Coursera: https://www.coursera.org/specializations/business-english",
    "crm": "CRM Fundamentals - Salesforce Trailhead: https://trailhead.salesforce.com/",
    "statist": "Statistics with R - Coursera: https://www.coursera.org/specializations/statistics",
    "scienc": "Data Science - Coursera: https://www.coursera.org/specializations/jhu-data-science",
    "model": "Machine Learning Models - Coursera: https://www.coursera.org/learn/machine-learning-models",
    "prototyp": "Prototyping - Coursera: https://www.coursera.org/learn/prototyping-design",
    "sketch": "Sketch for UX Design - Udemy: https://www.udemy.com/course/sketch-design/",
    "analysi": "Data Analysis - Coursera: https://www.coursera.org/specializations/data-analysis",
    "requir": "Requirements Engineering - Coursera: https://www.coursera.org/learn/requirements-engineering",
    "excel": "Excel Skills for Business - Coursera: https://www.coursera.org/specializations/excel",
    "c": "C Programming - Udemy: https://www.udemy.com/course/c-programming-for-beginners-/",
    "iot": "IoT Specialization - Coursera: https://www.coursera.org/specializations/internet-of-things",
    "electr": "Electronics for Beginners - Udemy: https://www.udemy.com/course/electronics-for-beginners/",
    "mechan": "Mechanical Engineering - Coursera: https://www.coursera.org/specializations/mechanical-engineering",
    "cad": "AutoCAD Basics - Udemy: https://www.udemy.com/course/autocad-2d-and-3d-practice-drawings/",
    "solidwork": "SolidWorks - Udemy: https://www.udemy.com/course/solidworks-course/",
    "autocad": "AutoCAD Complete Course - Udemy: https://www.udemy.com/course/the-complete-autocad-2019-course/",
    "bim": "BIM Fundamentals - Coursera: https://www.coursera.org/learn/bim-fundamentals",
    "revit": "Revit Architecture - Udemy: https://www.udemy.com/course/revit-architecture-2019/",
    "etl": "ETL Testing - Udemy: https://www.udemy.com/course/etl-testing-using-talend/",
    "spark": "Apache Spark - Udemy: https://www.udemy.com/course/apache-spark-with-scala-hands-on-with-big-data/",
    "hadoop": "Hadoop Tutorial - Udemy: https://www.udemy.com/course/the-ultimate-hands-on-hadoop/",
    "financ": "Financial Markets - Coursera: https://www.coursera.org/learn/financial-markets-global",
    "bank": "Banking Basics - Khan Academy: https://www.khanacademy.org/economics-finance-domain",
    "market": "Digital Marketing - Coursera: https://www.coursera.org/specializations/digital-marketing",
    "product": "Product Management - Coursera: https://www.coursera.org/specializations/product-management",
    "present": "Presentation Skills - Coursera: https://www.coursera.org/learn/presentation-skills",
    "technic": "Technical Communication - Coursera: https://www.coursera.org/learn/technical-writing",
    "microcontrol": "Microcontroller Programming - Udemy: https://www.udemy.com/course/microcontroller-embedded-c-programming/",
    "rtos": "RTOS Fundamentals - Udemy: https://www.udemy.com/course/freertos-on-arm-processors/",
    "qualiti": "Quality Management - Coursera: https://www.coursera.org/learn/quality-management",
    "process": "Business Process Management - Coursera: https://www.coursera.org/learn/business-process-management",
    "manufactur": "Manufacturing Engineering - Coursera: https://www.coursera.org/learn/manufacturing-engineering",
}

